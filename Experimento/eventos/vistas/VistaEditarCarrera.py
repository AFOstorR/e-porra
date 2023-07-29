
from flask import request,make_response
from flask_restful import Resource
from dto.errorDTO import ErrorResponse
from dto.eventoDTO import EventoDTO
from servicios.servicioCarreras import ServicioCarrera


class VistaEditarCarrera(Resource):
    servicioCarrera=ServicioCarrera()
    eventoDto=EventoDTO()
    def editarCarrera(self,id_evento):
        carrera=self.servicioCarrera.getCarrera(id_evento)
        if(carrera==None):
            return ErrorResponse().response("El evento que desea eliminar no existe")
        self.servicioCarrera.editCarrera(carrera=carrera,competidores=request.json["competidores"])
        
        return self.eventoDto.dump(carrera)