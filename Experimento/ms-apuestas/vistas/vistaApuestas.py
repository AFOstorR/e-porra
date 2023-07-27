import re
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
import datetime as dt
from modelos import db, Apuesta, ApuestaSchema, Usuario, UsuarioSchema, CompetidorSchema, \
    Competidor, ReporteSchema, EventoSchema, Evento, Transaccion, TransaccionSchema, TipoTransaccion

apuesta_schema = ApuestaSchema()
evento_schema = EventoSchema()
competidor_schema = CompetidorSchema()
usuario_schema = UsuarioSchema()
reporte_schema = ReporteSchema()
transaccion_schema = TransaccionSchema()

class VistaApuestas(Resource):
    def post(self,id_apostador):
        
        nueva_apuesta = Apuesta(valor_apostado=request.json["valor_apostado"],
                                nombre_apostador=request.json["nombre_apostador"],
                                id_competidor=request.json["id_competidor"] if request.json["id_competidor"] else None, 
                                id_evento=request.json["id_evento"])
        
        db.session.add(nueva_apuesta)
        fecha_transaccion = dt.datetime.now()
        transaccion = Transaccion(
            tipo_transaccion = TipoTransaccion.APUESTA,
            descripcion = 'Apuesta en evento {}'.format(Evento.query.filter(Evento.id == request.json["id_evento"])[0].nombre_evento),
            fecha = fecha_transaccion,
            es_leido = True,
            valor = - float(request.json['valor_apostado']),
            id_usuario = id_apostador
        )
        db.session.add(transaccion)
        apostador = Usuario.query.filter(Usuario.id == id_apostador)[0]
        apostador.monedero -= float(request.json['valor_apostado'])
        if len(Usuario.query.filter(Usuario.es_apostador == False).all()) > 0:
            usuario_administrador = Usuario.query.filter(Usuario.es_apostador == False).all()[0]
            transaccion = Transaccion(
                tipo_transaccion = TipoTransaccion.APUESTA,
                descripcion = 'Apuesta en evento {}'.format(Evento.query.filter(Evento.id == request.json["id_evento"])[0].nombre_evento),
                fecha = fecha_transaccion,
                es_leido = True,
                valor = float(request.json['valor_apostado']),
                id_usuario = usuario_administrador.id
            )
            db.session.add(transaccion)
            usuario_administrador.monedero += float(request.json['valor_apostado'])
            db.session.add(transaccion)
        db.session.commit()
        return usuario_schema.dump(Usuario.query.filter(Usuario.id == id_apostador)[0])
        #return apuesta_schema.dump(nueva_apuesta)

    def get(self, id_apostador):
        usuario_actual = Usuario.query.get_or_404(id_apostador)
        
        if usuario_actual.es_apostador:
            return [apuesta_schema.dump(ca) for ca in Apuesta.query.filter(Apuesta.nombre_apostador == usuario_actual.nombre).order_by(Apuesta.valor_apostado.desc()).all()]
        return [apuesta_schema.dump(ca) for ca in Apuesta.query.order_by(Apuesta.valor_apostado.desc()).all() ]
