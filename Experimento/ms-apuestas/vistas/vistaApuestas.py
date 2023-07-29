from flask import request
from flask_restful import Resource
from servicio.servicioApuestas import ServicioApuestas
    
class VistaApuestas(Resource):
    def post(self,id_apostador):
        servicioApuestas = ServicioApuestas()
        return servicioApuestas.createApuesta(id_apostador, request.json)

    def get(self, id_apostador):
        servicioApuestas = ServicioApuestas()
        return servicioApuestas.getApuestas(id_apostador)

