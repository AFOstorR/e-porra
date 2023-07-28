import json
import os
from flask_restful import Resource
from google.cloud import pubsub_v1

class PublicadorGoogle(Resource):
    crepential_path= os.getcwd()+"/"+"grupo-5-modernizacion-1d4ef81d1d68.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = crepential_path
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("grupo-5-modernizacion", "Notificacion")

    def notificar(self, message):
        message_bytes = message.encode('utf-8')
        try:
            publish_future = self.publisher.publish(self.topic_path, data=message_bytes)
      
        
        except Exception as e:
            print('Error al momento de publicar')
            print(e)
            return e