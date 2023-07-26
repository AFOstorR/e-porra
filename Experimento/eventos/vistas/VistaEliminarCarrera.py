import re
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime as dt
from modelos import db, CompetidorSchema, Competidor, EventoSchema, Evento
evento_schema = EventoSchema()

class VistaEliminarCarrera(Resource):
    @jwt_required()
    def eliminarCarrera(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        db.session.delete(evento)
        db.session.commit()
        return '', 204

