from email.policy import default
from flask_sqlalchemy import SQLAlchemy

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

