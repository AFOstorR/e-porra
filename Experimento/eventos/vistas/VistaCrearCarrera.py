import re
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime as dt
from modelos import db, Apuesta, ApuestaSchema, Usuario, UsuarioSchema, CompetidorSchema, \
    Competidor, ReporteSchema, EventoSchema, Evento, Transaccion, TransaccionSchema, TipoTransaccion


evento_schema = EventoSchema()

class VistaCrearCarrera(Resource):

    @jwt_required()
    def crearCarrera(self, id_usuario):
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


