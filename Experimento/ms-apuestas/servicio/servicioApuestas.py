from dtos.dtos import ApuestaDTO, UsuarioDTO
from modelos.modelos import Apuesta, Transaccion, Usuario, TipoTransaccion, Evento, db
from servicio.servicioTransaccion import ServicioTransaccion
import datetime as dt

class ServicioApuestas:

    def getApuesta(self, id_apuesta):
        apuestaDTO = ApuestaDTO()
        return apuestaDTO.dump(Apuesta.query.get_or_404(id_apuesta))

    def putApuesta(self, id_apuesta, requestJson):
        apuestaDTO = ApuestaDTO()
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        apuesta.valor_apostado = requestJson.get("valor_apostado", apuesta.valor_apostado)
        apuesta.nombre_apostador = requestJson.get("nombre_apostador", apuesta.nombre_apostador)
        apuesta.id_competidor = requestJson.get("id_competidor", apuesta.id_competidor)
        apuesta.id_evento = requestJson.get("id_evento", apuesta.id_evento)
        db.session.commit()
        return apuestaDTO.dump(apuesta)
    
    def deleteApuesta(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        db.session.delete(apuesta)
        db.session.commit()
        return '', 204
    
    def createApuesta(self, id_apostador, requestJson):
        usuarioDTO = UsuarioDTO()
        servicioTransaccion = ServicioTransaccion()
        nueva_apuesta = Apuesta(valor_apostado=requestJson["valor_apostado"],
                                nombre_apostador=requestJson["nombre_apostador"],
                                id_competidor=requestJson["id_competidor"] if requestJson["id_competidor"] else None, 
                                id_evento=requestJson["id_evento"])
        db.session.add(nueva_apuesta)
        servicioTransaccion.transaccionApuestaApostador(id_apostador, requestJson)
        servicioTransaccion.transaccionApuestaCasa(requestJson)
        return usuarioDTO.dump(Usuario.query.filter(Usuario.id == id_apostador)[0])
    
    def getApuestas(self, id_apostador):
        apuestaDTO = ApuestaDTO()
        usuario = Usuario.query.get_or_404(id_apostador)
        if usuario.es_apostador:
            return [apuestaDTO.dump(ca) for ca in Apuesta.query.filter(Apuesta.nombre_apostador == usuario.nombre).order_by(Apuesta.valor_apostado.desc()).all()]
        return [apuestaDTO.dump(ca) for ca in Apuesta.query.order_by(Apuesta.valor_apostado.desc()).all() ]

