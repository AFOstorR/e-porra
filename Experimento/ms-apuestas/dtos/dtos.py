from modelos.modelos import Apuesta, Competidor, Evento, Usuario, Transaccion
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ApuestaDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = Apuesta
        include_relationships = True
        include_fk = True
        load_instance = True

    valor_apostado = fields.String()
    ganancia = fields.String()


class CompetidorDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = Competidor
        include_relationships = True
        load_instance = True

    probabilidad = fields.String()
    cuota = fields.String()


class EventoDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = Evento
        include_relationships = True
        load_instance = True

    competidores = fields.List(fields.Nested(CompetidorDTO()))
    apuestas = fields.List(fields.Nested(ApuestaDTO()))
    ganancia_casa = fields.Float()


class UsuarioDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('contrasena',)


class ReporteDTO(Schema):
    evento = fields.Nested(EventoDTO())
    ganancia_casa = fields.Float()

class TransaccionDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = Transaccion
        include_relationships = True
        load_instance = True