
from email.policy import default
from flask.json import jsonify
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modelos import Evento
from .competidorDTO import ApuestaDTO,CompetidorDTO
from flask import make_response, jsonify

class EventoDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = Evento
        include_relationships = True
        load_instance = True

    competidores = fields.List(fields.Nested((CompetidorDTO)))
    apuestas = fields.List(fields.Nested(ApuestaDTO()))
    ganancia_casa = fields.Float()


class ListEventosDTO():
    def listaEventos(self,lista):
        resp=make_response(jsonify([EventoDTO().dump( ev )for ev in lista]))
        resp.status_code=200
        return resp

