
from flask import request,make_response
from flask_restful import Resource
from dto.errorDTO import ErrorResponse
from dto.eventoDTO import EventoDTO
from servicios.servicioCarreras import ServicioCarrera





class VistaCrearCarrera(Resource):
    servicioCarrera=ServicioCarrera()
    def crearCarrera(self, id_usuario):
        nuevoEvento=self.servicioCarrera.crearCarrera(request=request,id_usuario=id_usuario)
        if(nuevoEvento==None):
            return ErrorResponse().response('El usuario ya tiene un carrera con dicho nombre', 409)
        return EventoDTO().dump(nuevoEvento)
        


