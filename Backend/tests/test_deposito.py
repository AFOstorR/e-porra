import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app


class TestTransacciones(TestCase):

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
        self.usuario_test = respuesta_al_crear_usuario['usuario']
    
    def test_deposito_no_vacio(self):
        datos_transaccion = {
            "valor": " ",
            "tipo_transaccion": "DEPOSITO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_deposito = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_deposito.status_code, 409)
    
    def test_deposito_valor_numerico(self):
        datos_transaccion = {
            "valor": self.data_factory.word(),
            "tipo_transaccion": "DEPOSITO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_deposito = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)
        self.assertEqual(solicitud_deposito.status_code, 409)

    def test_deposito_minimo_5000(self):
        datos_transaccion = {
            "valor": random.random()*4999,
            "tipo_transaccion": "DEPOSITO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_deposito = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_deposito.status_code, 409)

    def test_deposito_exitoso(self):
        datos_transaccion = {
            "valor": 5000 + random.random()*10000,
            "tipo_transaccion": "DEPOSITO"
        }

        endpoint_update = "/transaccion/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_deposito = self.client.post(endpoint_update,
                                                   data=json.dumps(datos_transaccion),
                                                   headers=headers)

        self.assertEqual(solicitud_deposito.status_code, 200)

    def tearDown(self):
        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        self.client.delete(endpoint_update, headers=headers)

