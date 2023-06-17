from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum

db = SQLAlchemy()

class TipoTransaccion(str, enum.Enum):
    DEPOSITO = 'DEPOSITO'
    RETIRO = 'RETIRO'
    GANANCIA = 'GANANCIA'
    APUESTA = 'APUESTA'

class Apuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor_apostado = db.Column(db.Numeric)
    ganancia = db.Column(db.Numeric, default=0)
    nombre_apostador = db.Column(db.String(128))
    id_competidor = db.Column(db.Integer, db.ForeignKey('competidor.id'), nullable=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'))

class TipoEvento(str,enum.Enum):
    CARRERA = 'CARRERA'
    MARCADOR = 'MARCADOR'

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.String(128))
    abierta = db.Column(db.Boolean, default=True)
    competidores = db.relationship('Competidor', cascade='all, delete, delete-orphan')
    apuestas = db.relationship('Apuesta', cascade='all, delete, delete-orphan')
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    es_empate = db.Column(db.Boolean,default=False)
    tipo_evento = db.Column(db.Enum(TipoEvento))


class Competidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_competidor = db.Column(db.String(128))
    probabilidad = db.Column(db.Numeric)
    cuota = db.Column(db.Numeric)
    es_ganador = db.Column(db.Boolean, default=False)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'))


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True)
    contrasena = db.Column(db.String(50))
    eventos = db.relationship('Evento', cascade='all, delete, delete-orphan')
    es_apostador = db.Column(db.Boolean,default=True) 
    nombre = db.Column(db.String(50))
    numero_tarjeta = db.Column(db.String(16))
    monedero = db.Column(db.Float, default=0)
    transacciones = db.relationship('Transaccion', cascade='all, delete, delete-orphan')


class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_transaccion = db.Column(db.Enum(TipoTransaccion))
    descripcion = db.Column(db.String(100))
    fecha = db.Column(db.DateTime)
    es_leido = db.Column(db.Boolean, default = True)
    valor = db.Column(db.Float)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))


class ApuestaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Apuesta
        include_relationships = True
        include_fk = True
        load_instance = True

    valor_apostado = fields.String()
    ganancia = fields.String()


class CompetidorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Competidor
        include_relationships = True
        load_instance = True

    probabilidad = fields.String()
    cuota = fields.String()


class EventoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Evento
        include_relationships = True
        load_instance = True

    competidores = fields.List(fields.Nested(CompetidorSchema()))
    apuestas = fields.List(fields.Nested(ApuestaSchema()))
    ganancia_casa = fields.Float()


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('contrasena',)


class ReporteSchema(Schema):
    evento = fields.Nested(EventoSchema())
    ganancia_casa = fields.Float()

class TransaccionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transaccion
        include_relationships = True
        load_instance = True