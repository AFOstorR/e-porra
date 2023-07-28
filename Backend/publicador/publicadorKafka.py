import json
import os
from flask_restful import Resource
from kafka import KafkaProducer 

class PublicadorKafka(Resource):
    producer = KafkaProducer(
        bootstrap_servers=[os.environ.get('BROKER_PATH','')],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
  
    def notificar(self, message):
        self.producer.send('Notificar', message)
        self.producer.flush()