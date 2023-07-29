from flask import make_response
from flask_restful import Resource
from dto.errorDTO import ErrorResponse
from dto.eventoDTO import EventoDTO
from servicios.servicioCarreras import ServicioCarrera

class VistaEliminarCarrera(Resource):
    servicoCarrera=ServicioCarrera()
    def eliminarCarrera(self,idEvento):
        evento =self.servicoCarrera.getCarrera(id_evento=idEvento)    
        if(evento==None):
            return ErrorResponse().response("El evento que desea eliminar no existe")
        self.servicoCarrera.deleteCarrera(evento)
        return 'El evento  ha sido eliminada correctamente', 204

