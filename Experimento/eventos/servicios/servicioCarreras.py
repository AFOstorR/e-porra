


from modelos import Evento,db,Usuario
from .servicioCompetidores import ServicioCompetidores
from sqlalchemy.exc import IntegrityError
class ServicioCarrera:
    
    def getCarrera(self,id_evento):
        return Evento.query.filter(Evento.id==id_evento).first()
    
    def getCarreras(self):
        return Evento.query.all()
    
    def editCarrera(self,carrera,competidores):
        servicioCompetidor=ServicioCompetidores()
        print(competidores)
        carrera.competidores=servicioCompetidor.agregarCompetidores(competidores,carrera.id)

        db.session.commit()
    
    def deleteCarrera(self,carrera):
        db.session.delete(carrera)
        db.session.commit()
    
    def crearCarrera(self,request,id_usuario):
        nuevo_evento = Evento(nombre_evento=request.json["nombre"],
                              tipo_evento = request.json['tipo_evento']  
        )
        servicioCompetidor=ServicioCompetidores()
        nuevo_evento.competidores=servicioCompetidor.agregarCompetidores(competidores=request.json["competidores"],idevento=nuevo_evento.id)

        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.eventos.append(nuevo_evento)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return nuevo_evento