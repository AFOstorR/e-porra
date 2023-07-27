import re
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime as dt
from modelos import db, Apuesta, ApuestaSchema, Usuario, UsuarioSchema, CompetidorSchema, \
    Competidor, ReporteSchema, EventoSchema, Evento, Transaccion, TransaccionSchema, TipoTransaccion
from publicador.publicadorKafka import PublicadorKafka


apuesta_schema = ApuestaSchema()
evento_schema = EventoSchema()
competidor_schema = CompetidorSchema()
usuario_schema = UsuarioSchema()
reporte_schema = ReporteSchema()
transaccion_schema = TransaccionSchema()

class VistaSignIn(Resource):

    def post(self):
        request_usuario = request.json
        for campo, valor in request_usuario.items():
            if campo != 'es_apostador':
                if type(valor) is not str:
                    return 'El campo %s no es de tipo string' %(campo), 400
                if len(valor) == 0 or len(valor) > 50:
                    if campo == 'numero_tarjeta' and len(valor) != 16:
                        return 'El campo %s debe tener una longitud de 16 caracteres' %(campo), 400
                    return 'El campo %s está vacio o excede la longitud permitida (50 caracteres)' %(campo), 400
        if  ("es_apostador" in request_usuario) and (request_usuario['es_apostador'] == False) and (len(Usuario.query.filter(Usuario.es_apostador==False).all())>0):
            return {"mensaje": "usuario ya existente", 
                "token": create_access_token(identity=Usuario.query.filter(Usuario.es_apostador==False).all()[0].id), 
                "id": Usuario.query.filter(Usuario.es_apostador==False).all()[0].id, "nombre": Usuario.query.filter(Usuario.es_apostador==False).all()[0].usuario, 
                "es_apostador": Usuario.query.filter(Usuario.es_apostador==False).all()[0].es_apostador, 
                "usuario": usuario_schema.dump(Usuario.query.filter(Usuario.es_apostador==False).all()[0])
                }
        nuevo_usuario = Usuario(usuario=request_usuario["usuario"], contrasena=request_usuario["contrasena"],\
            nombre = request_usuario["nombre"], numero_tarjeta = request_usuario["numero_tarjeta"],
            es_apostador = request_usuario['es_apostador'] if "es_apostador" in request_usuario else True)
            
        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
            token_de_acceso = create_access_token(identity=nuevo_usuario.id)
            return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id, "nombre": nuevo_usuario.usuario, "es_apostador": nuevo_usuario.es_apostador, "usuario": usuario_schema.dump(nuevo_usuario)}
        except IntegrityError:
            return 'El correo %s ya se encuentra registrado.' %(request_usuario['usuario']) , 400


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "usuario": usuario_schema.dump(usuario)}

class VistaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))

    @jwt_required()
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        request_usuario = request.json 
        if len(request_usuario['correo_electronico'].strip()) == 0:
            return 'El correo no debe estar vacío', 409
        elif not re.search('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$', request_usuario['correo_electronico']):   
            return 'El correo debe tener formato válido', 409
        elif len(request_usuario['numero_tarjeta'].strip()) == 0:
            return 'El numero de tarjeta no debe estar vacío', 409
        elif len(request_usuario['numero_tarjeta']) != 16:
            return('El numero de tarjeta debe tener exactamente 16 caracteres', 409)
        else:
            try: 
                usuario.usuario = request_usuario.get("correo_electronico", usuario.usuario)
                usuario.numero_tarjeta = request_usuario.get("numero_tarjeta", usuario.numero_tarjeta)
                db.session.commit()
            except Exception:
                return('El correo ya existe', 400)
            return usuario_schema.dump(usuario)

    @jwt_required()
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204



class VistaCarrerasUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_evento = Evento(nombre_evento=request.json["nombre"],
                              tipo_evento = request.json['tipo_evento']  
        )

        for item in request.json["competidores"]:
            cuota = round((item["probabilidad"] / (1 - item["probabilidad"])), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=item["probabilidad"],
                                    cuota=cuota,
                                    id_evento=nuevo_evento.id)
            nuevo_evento.competidores.append(competidor)     
        
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.eventos.append(nuevo_evento)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un carrera con dicho nombre', 409

        return evento_schema.dump(nuevo_evento)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [evento_schema.dump(evento) for evento in usuario.eventos]


class VistaCarreras(Resource):
    @jwt_required()
    def get(self):
        return [evento_schema.dump( ev )for ev in Evento.query.all()]

class VistaCarrera(Resource):

    @jwt_required()
    def get(self, id_evento):
        return evento_schema.dump(Evento.query.get_or_404(id_evento))

    @jwt_required()
    def put(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        evento.nombre_evento = request.json.get("nombre", evento.nombre_evento)
        evento.competidores = []
        evento.tipo_evento = request.json.get("tipo_evento",evento.tipo_evento)
        
        for item in request.json["competidores"]:
            probabilidad = float(item["probabilidad"])
            cuota = round((probabilidad / (1 - probabilidad)), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=probabilidad,
                                    cuota=cuota,
                                    id_evento=evento.id)
            evento.competidores.append(competidor)



        db.session.commit()
        return evento_schema.dump(evento)

    @jwt_required()
    def delete(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        db.session.delete(evento)
        db.session.commit()
        return '', 204

class VistaApuestas(Resource):
    def post(self,id_apostador):
        publicador = PublicadorKafka()
        publicador.notificar({'id_apostador': id_apostador, 'request': request.json})


    @jwt_required()
    def get(self, id_apostador):
        usuario_actual = Usuario.query.get_or_404(id_apostador)
        
        if usuario_actual.es_apostador:
            return [apuesta_schema.dump(ca) for ca in Apuesta.query.filter(Apuesta.nombre_apostador == usuario_actual.nombre).order_by(Apuesta.valor_apostado.desc()).all()]
        return [apuesta_schema.dump(ca) for ca in Apuesta.query.order_by(Apuesta.valor_apostado.desc()).all() ]


class VistaApuesta(Resource):
    @jwt_required()
    def get(self, id_apuesta):
        return apuesta_schema.dump(Apuesta.query.get_or_404(id_apuesta))

    @jwt_required()
    def put(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        apuesta.valor_apostado = request.json.get("valor_apostado", apuesta.valor_apostado)
        apuesta.nombre_apostador = request.json.get("nombre_apostador", apuesta.nombre_apostador)
        apuesta.id_competidor = request.json.get("id_competidor", apuesta.id_competidor)
        apuesta.id_evento = request.json.get("id_evento", apuesta.id_evento)
        db.session.commit()
        return apuesta_schema.dump(apuesta)

    @jwt_required()
    def delete(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        db.session.delete(apuesta)
        db.session.commit()
        return '', 204


class VistaTerminacionCarrera(Resource):

    def put(self, id_competidor):
        competidor = Competidor.query.get_or_404(id_competidor)
        competidor.es_ganador = True
        evento = Evento.query.get_or_404(competidor.id_evento)
        evento.abierta = False
        total_casa = 0
        usuario_administrador = Usuario.query.filter(Usuario.es_apostador == False).all()[0]
        
        for apuesta in evento.apuestas:
            apuesta.ganancia = (apuesta.valor_apostado + (apuesta.valor_apostado/competidor.cuota)) * (apuesta.id_competidor == competidor.id)
            usuario = Usuario.query.filter(Usuario.nombre == apuesta.nombre_apostador).all()[0]
            transaccion = Transaccion( tipo_transaccion = TipoTransaccion.GANANCIA, 
                descripcion = 'Felicitaciones! Has ganado $ {:,.2f}  por tu apuesta en {}'.format(round(apuesta.ganancia, 2), evento.nombre_evento) if round(apuesta.ganancia,2)>0 else 'El evento {} ha finalizado. Tu ganancia fue $0.00'.format(evento.nombre_evento),
                valor = apuesta.ganancia,
                fecha = dt.datetime.now(),
                id_usuario = usuario.id,
                es_leido = False
                )
            usuario.monedero += float(apuesta.ganancia)
            total_casa -= float(apuesta.ganancia)
            db.session.add(transaccion)
        
        transaccion = Transaccion(tipo_transaccion = TipoTransaccion.GANANCIA,
            descripcion = 'Pérdida por pago de ganancias a apostadores.',
            valor = total_casa,
            fecha = dt.datetime.now(),
            id_usuario = usuario_administrador.id)
        usuario_administrador.monedero += total_casa
        db.session.add(transaccion)

        db.session.commit()
        return competidor_schema.dump(competidor)


class VistaReporte(Resource):

    @jwt_required()
    def get(self, id_evento):
        evento_reporte = Evento.query.get_or_404(id_evento)
        ganancia_casa_final = 0

        for apuesta in evento_reporte.apuestas:
            ganancia_casa_final = ganancia_casa_final + apuesta.valor_apostado - apuesta.ganancia

        reporte = dict(evento=evento_reporte, ganancia_casa=ganancia_casa_final)
        schema = ReporteSchema()
        return schema.dump(reporte)


class VistaTransaccion(Resource):
    @jwt_required()
    def post(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        request_transaccion = request.json
        
        if len(str(request_transaccion['valor']).strip()) == 0:
            return 'El valor no debe estar vacío', 409
        elif not str(request_transaccion['valor']).replace('.', '').replace('-','').isnumeric():
            return 'El valor debe ser numérico', 409
        elif float(request_transaccion['valor']) <= 0:
            return 'La transacción debe ser mayor a 0', 409
        elif request_transaccion['tipo_transaccion'] == 'DEPOSITO':
            if float(request_transaccion['valor']) < 5000:
                return 'El valor mínimo es de $5000', 409
            else:
                valor_transaccion =  float(request_transaccion['valor'])
                descripcion_transaccion = 'Depósito de dinero'
        elif request_transaccion['tipo_transaccion'] == 'RETIRO':
            if float(request_transaccion['valor']) > usuario.monedero:
                return 'El valor máximo es el disponible', 409
            else:
                valor_transaccion = - float(request_transaccion['valor'])
                descripcion_transaccion = 'Retiro de dinero'
        elif request_transaccion['tipo_transaccion'] == 'GANANCIA':
            valor_transaccion = - float(request_transaccion['valor'])
            descripcion_transaccion = 'Apuesta en la carrera'
        
        nueva_transaccion = Transaccion(tipo_transaccion = request_transaccion['tipo_transaccion'], descripcion = descripcion_transaccion,
                                valor = valor_transaccion, fecha = dt.datetime.now(), id_usuario = id_usuario)
        db.session.add(nueva_transaccion)
        usuario.monedero += valor_transaccion
        db.session.commit()
        return usuario_schema.dump(usuario)

    @jwt_required()
    def get(self, id_usuario):
        return [transaccion_schema.dump(tr) for tr in Transaccion.query.filter(Transaccion.id_usuario == id_usuario).order_by(Transaccion.fecha.desc()).all()]


    @jwt_required()
    def put(self, id_usuario):
        transaccion = Transaccion.query.get_or_404(id_usuario)
        transaccion.es_leido = 1
        db.session.commit()
        return transaccion_schema.dump(transaccion)
        
class VistaApostadores(Resource):
    @jwt_required()
    def get(self):
        return [usuario_schema.dump(u) for u in Usuario.query.filter(Usuario.es_apostador == True).all()]    