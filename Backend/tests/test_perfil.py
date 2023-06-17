import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app


class TestPerfil(TestCase):

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
    
    def test_actualizar_perfil_correo_no_vacio(self):
   
        datos_nuevos = {
            "correo_electronico": " ",
            "numero_tarjeta": "1234567812345678"
        }

        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_actualizar_perfil = self.client.put(endpoint_update,
                                                   data=json.dumps(datos_nuevos),
                                                   headers=headers)

        self.assertEqual(solicitud_actualizar_perfil.status_code, 409)

    def test_actualizar_perfil_correo_valido(self):
   
        datos_nuevos = {
            "correo_electronico": self.data_factory.word(),
            "numero_tarjeta": "1234567812345678",
        }

        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        solicitud_actualizar_perfil = self.client.put(endpoint_update,
                                                   data=json.dumps(datos_nuevos),
                                                   headers=headers)
        self.assertEqual(solicitud_actualizar_perfil.status_code, 409)

    def test_actualizar_perfil_numero_tarjeta_no_vacio(self):
   
        datos_nuevos = {
            "correo_electronico": self.data_factory.email(),
            "numero_tarjeta": "  ",
        }

        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        solicitud_actualizar_perfil = self.client.put(endpoint_update,
                                                   data=json.dumps(datos_nuevos),
                                                   headers=headers)
        self.assertEqual(solicitud_actualizar_perfil.status_code, 409)

    def test_actualizar_perfil_numero_tarjeta_de_16_caracteres (self):
   
        datos_nuevos = {
            "correo_electronico": self.data_factory.email(),
            "numero_tarjeta": self.data_factory.word() * 16,
        }
        
        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        solicitud_actualizar_perfil = self.client.put(endpoint_update,
                                                   data=json.dumps(datos_nuevos),
                                                   headers=headers)
        self.assertEqual(solicitud_actualizar_perfil.status_code, 409)

    def test_actualizar_perfil_exitoso (self):
   
        datos_nuevos = {
            "correo_electronico": self.data_factory.email(),
            "numero_tarjeta": "1"*16,
        }
        
        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        solicitud_actualizar_perfil = self.client.put(endpoint_update,
                                                   data=json.dumps(datos_nuevos),
                                                   headers=headers)
        self.assertEqual(solicitud_actualizar_perfil.status_code, 200)

    



    def tearDown(self):
        endpoint_update = "/usuario/{}".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        self.client.delete(endpoint_update, headers=headers)

