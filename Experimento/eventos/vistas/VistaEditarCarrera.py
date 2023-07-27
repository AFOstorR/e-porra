import re
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime as dt
from modelos import db, CompetidorSchema, Competidor, EventoSchema, Evento
evento_schema = EventoSchema()
class VistaEditarCarrera(Resource):

    def editarCarrera(id_evento):
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