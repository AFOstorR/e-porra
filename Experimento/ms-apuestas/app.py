import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas.vistaApuestas import VistaApuestas
from vistas.vistaApuesta import VistaApuesta
from obtenerApuestas.obtenerApuesta import ObtenerApuesta

suscriptor = ObtenerApuesta()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///../../eporra.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaApuestas, '/apuestas/<int:id_apostador>')
api.add_resource(VistaApuesta, '/apuesta/<int:id_apuesta>')
suscriptor.recibirApuesta()