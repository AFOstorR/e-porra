import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app


class TestRetiro(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.email(),
            "nombre": self.data_factory.name(),
            "contrasena": self.data_factory.password(),
            "numero_tarjeta": str(self.data_factory.random_number(digits=16)),
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]
        
        datos_transaccion = {
            "valor": 5000 + random.random()*10000,
            "tipo_transaccion": "DEPOSITO"
        }
        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_deposito = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)
        self.usuario_test = json.loads(solicitud_deposito.get_data())

 
    def test_retiro_no_vacio(self):
        datos_transaccion = {
            "valor": " ",
            "tipo_transaccion": "RETIRO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_retiro = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_retiro.status_code, 409)
    
    def test_retiro_valor_numerico(self):
        datos_transaccion = {
            "valor": self.data_factory.word(),
            "tipo_transaccion": "RETIRO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_retiro = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)
        self.assertEqual(solicitud_retiro.status_code, 409)

    def test_retiro_mayor_0(self):
        datos_transaccion = {
            "valor": -random.random(),
            "tipo_transaccion": "RETIRO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_retiro = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_retiro.status_code, 409)
    
    def test_retiro_maximo_disponible(self):
        datos_transaccion = {
            "valor": float(self.usuario_test['monedero'])+ random.random() * 5000,
            "tipo_transaccion": "RETIRO"
        }
        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_retiro = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_retiro.status_code, 409)

    def test_retiro_exitoso(self):
        datos_transaccion = {
            "valor": random.random() * self.usuario_test['monedero'],
            "tipo_transaccion": "RETIRO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_retiro = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_retiro.status_code, 200)


    def tearDown(self):
        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        self.client.delete(endpoint_update, headers=headers)

