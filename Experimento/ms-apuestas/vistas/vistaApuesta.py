from flask import request
from flask_restful import Resource
from servicio.servicioApuestas import ServicioApuestas

class VistaApuesta(Resource):
    
    def get(self, id_apuesta):
        servicioApuestas = ServicioApuestas()
        return servicioApuestas.getApuesta(id_apuesta)

    
    def put(self, id_apuesta):
        servicioApuestas = ServicioApuestas()        
        return servicioApuestas.putApuesta(id_apuesta, request.json)

    def delete(self, id_apuesta):
        servicioApuestas = ServicioApuestas()
        return servicioApuestas.deleteApuesta(id_apuesta)