from flask import Flask,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas import VistaGetCarrera,VistaCrearCarrera,VistaEditarCarrera,VistaEliminarCarrera
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eporra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

@app.route("/carrera/<int:idEvento>",methods=["GET"])
def getCarrera(idEvento):
    return VistaGetCarrera.getCarrera(idEvento)

@app.route("/carreras",methods=["GET"])
def getEventos():
    return jsonify(VistaGetCarrera.getCarreras())

@app.route("/usuario/<int:id_usuario>/carreras",methods=["POST"])
def crearEvento(id_usuario):
    return VistaCrearCarrera.crearCarrera(id_usuario)

@app.route("/carrera/<int:idEvento>",methods=["DELETE"])
def eliminarEvento(idEvento):
    return VistaEliminarCarrera.eliminarCarrera(idEvento)

@app.route("/carrera/<int:idEvento>",methods=["PUT"])
def editarEvento(idEvento):
    return VistaEditarCarrera.editarCarrera(idEvento)

jwt = JWTManager(app)