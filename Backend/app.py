import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import os

from modelos import db
from vistas import VistaApuestas, VistaApuesta, VistaSignIn, VistaLogIn, VistaUsuario, \
    VistaCarrerasUsuario, VistaCarrera, VistaTerminacionCarrera, VistaReporte, VistaTransaccion,\
        VistaCarreras, VistaApostadores

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
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaCarrerasUsuario, '/usuario/<int:id_usuario>/carreras')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaCarrera, '/carrera/<int:id_evento>')
api.add_resource(VistaCarreras, '/carreras')
api.add_resource(VistaApuestas, '/apuestas/<int:id_apostador>')
api.add_resource(VistaApuesta, '/apuesta/<int:id_apuesta>')
api.add_resource(VistaTerminacionCarrera, '/carrera/<int:id_competidor>/terminacion')
api.add_resource(VistaReporte, '/carrera/<int:id_evento>/reporte')
api.add_resource(VistaTransaccion, '/transaccion/<int:id_usuario>')
api.add_resource(VistaApostadores, '/apostadores')


jwt = JWTManager(app)