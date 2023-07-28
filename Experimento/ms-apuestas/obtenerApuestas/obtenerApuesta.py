import json
import os
import datetime as dt
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from modelos import db, Apuesta, Transaccion, TipoTransaccion, Evento, Usuario

class ObtenerApuesta():
    # if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) is None:
    #     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credencial_google.json'
    # timeout = 5.0
    crepential_path= os.getcwd()+"/"+"grupo-5-modernizacion-1d4ef81d1d68.json"
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = crepential_path

    # subscription_path = os.environ.get('GOOGLE_APPLICATION_SUB_APUESTAS', None)
    
    def crearApuesta(self, message):
        apuestaJson = json.loads(message.data)['request']
        id_apostador = json.loads(message.data)['id_apostador']
        nueva_apuesta = Apuesta(valor_apostado = apuestaJson["valor_apostado"],
                                nombre_apostador = apuestaJson["nombre_apostador"],
                                id_competidor = apuestaJson["id_competidor"] if apuestaJson["id_competidor"] else None, 
                                id_evento = apuestaJson["id_evento"])
        
        db.session.add(nueva_apuesta)
        fecha_transaccion = dt.datetime.now()
        transaccion = Transaccion(
            tipo_transaccion = TipoTransaccion.APUESTA,
            descripcion = 'Apuesta en evento {}'.format(Evento.query.filter(Evento.id == apuestaJson["id_evento"])[0].nombre_evento),
            fecha = fecha_transaccion,
            es_leido = True,
            valor = - float(apuestaJson['valor_apostado']),
            id_usuario = id_apostador
        )
        db.session.add(transaccion)
        apostador = Usuario.query.filter(Usuario.id == id_apostador)[0]
        apostador.monedero -= float(apuestaJson['valor_apostado'])
        if len(Usuario.query.filter(Usuario.es_apostador == False).all()) > 0:
            usuario_administrador = Usuario.query.filter(Usuario.es_apostador == False).all()[0]
            transaccion = Transaccion(
                tipo_transaccion = TipoTransaccion.APUESTA,
                descripcion = 'Apuesta en evento {}'.format(Evento.query.filter(Evento.id == apuestaJson["id_evento"])[0].nombre_evento),
                fecha = fecha_transaccion,
                es_leido = True,
                valor = float(apuestaJson['valor_apostado']),
                id_usuario = usuario_administrador.id
            )
            db.session.add(transaccion)
            usuario_administrador.monedero += float(apuestaJson['valor_apostado'])
            db.session.add(transaccion)
        db.session.commit()
        
        message.ack()
    
    def recibirApuesta(self):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path("grupo-5-modernizacion", "Notificacion-sub")
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=self.crearApuesta)
        with subscriber:
            try:                
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()