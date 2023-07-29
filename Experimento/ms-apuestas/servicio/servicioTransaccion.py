from dtos.dtos import ApuestaDTO, UsuarioDTO
from modelos.modelos import Apuesta, Transaccion, Usuario, TipoTransaccion, Evento, db
import datetime as dt

class ServicioTransaccion:
    def transaccionApuestaApostador(self, id_apostador, requestJson):
        fecha_transaccion = dt.datetime.now()
        transaccion = Transaccion(
            tipo_transaccion = TipoTransaccion.APUESTA,
            descripcion = 'Apuesta en evento {}'.format(Evento.query.filter(Evento.id == requestJson["id_evento"])[0].nombre_evento),
            fecha = fecha_transaccion,
            es_leido = True,
            valor = - float(requestJson['valor_apostado']),
            id_usuario = id_apostador
        )
        db.session.add(transaccion)
    
        apostador = Usuario.query.filter(Usuario.id == id_apostador)[0]
        apostador.monedero -= float(requestJson['valor_apostado'])
    
    def transaccionApuestaCasa(self, requestJson):
        fecha_transaccion = dt.datetime.now()
        if len(Usuario.query.filter(Usuario.es_apostador == False).all()) > 0:
            usuario_administrador = Usuario.query.filter(Usuario.es_apostador == False).all()[0]
            transaccion = Transaccion(
                tipo_transaccion = TipoTransaccion.APUESTA,
                descripcion = 'Apuesta en evento {}'.format(Evento.query.filter(Evento.id == requestJson["id_evento"])[0].nombre_evento),
                fecha = fecha_transaccion,
                es_leido = True,
                valor = float(requestJson['valor_apostado']),
                id_usuario = usuario_administrador.id
            )
            db.session.add(transaccion)
            usuario_administrador.monedero += float(requestJson['valor_apostado'])
            db.session.add(transaccion)
        db.session.commit()