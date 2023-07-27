import json
import os
import datetime as dt
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from modelos import db, Apuesta, Transaccion, TipoTransaccion, Evento, Usuario
from json import loads
from kafka import KafkaConsumer
import os

class ObtenerApuesta:
    def enviarNotificacion(self):
        server = os.environ.get('SERVER_KAFKA', None)
        if server == None:
            server = 'localhost:9092'
        
        consumer = KafkaConsumer (
            'Notificar',
            bootstrap_servers = [server],
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            auto_commit_interval_ms=1000
        )
        for n in consumer:
            self.crearApuesta(n.value)
    
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