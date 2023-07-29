

from flask_restful import Resource
from servicios.servicioCarreras import ServicioCarrera
from dto.eventoDTO import EventoDTO,ListEventosDTO
from dto.errorDTO import ErrorResponse

class VistaGetCarrera(Resource):
    servicioCarrera=ServicioCarrera()
    eventoDto=EventoDTO()
    def getCarrera(self,idEvento):
        carrera=self.servicioCarrera.getCarrera(idEvento)
        if(carrera==None):
            return ErrorResponse().response("Evento no existe") 
        
        return self.eventoDto.dump(carrera)
        
     

    def getCarreras(self):
        carreras=self.servicioCarrera.getCarreras()
        
        return ListEventosDTO().listaEventos(carreras)
