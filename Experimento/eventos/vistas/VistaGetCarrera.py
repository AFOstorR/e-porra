import re
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime as dt
from modelos import  EventoSchema, Evento

evento_schema = EventoSchema()
class VistaGetCarrera(Resource):

    def getCarrera(id_evento):
        return evento_schema.dump(Evento.query.get_or_404(id_evento))

    def getCarreras():
        return [evento_schema.dump( ev )for ev in Evento.query.all()]
