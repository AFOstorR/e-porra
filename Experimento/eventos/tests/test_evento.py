import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app


class TestEvento(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.email(),
            "nombre": self.data_factory.name(),
            "contrasena": self.data_factory.password(),
            "numero_tarjeta": str(self.data_factory.random_number(digits=16))
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]

    def test_crear_evento(self):
        nuevo_evento = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": 'Empate'
                }
            ],
            "tipo_evento": "MARCADOR"
        }

        endpoint_eventos = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_evento = self.client.post(endpoint_eventos,
                                                   data=json.dumps(nuevo_evento),
                                                   headers=headers)

        self.assertEqual(solicitud_nuevo_evento.status_code, 200)

    def test_editar_evento(self):
        nuevo_evento_1 = {
            "nombre": "Sakhir. 57 vueltas",
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": 'Empate'
                }
             
            ],
            "tipo_evento": "MARCADOR"
        }

        nuevo_evento_2 = {
            "nombre": "Sakhir 130 vueltas",
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": 'Empate'
                }
            ],
            "tipo_evento": "MARCADOR"
        }

        endpoint_crear_evento = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_evento_1 = self.client.post(endpoint_crear_evento,
                                                     data=json.dumps(nuevo_evento_1),
                                                     headers=headers)

        respuesta_al_crear_evento = json.loads(solicitud_nuevo_evento_1.get_data())
        id_evento = respuesta_al_crear_evento["id"]

        endpoint_editar_evento = "/carrera/{}".format(str(id_evento))

        solicitud_editar_evento = self.client.put(endpoint_editar_evento,
                                                   data=json.dumps(nuevo_evento_2),
                                                   headers=headers)

        evento_editado = json.loads(solicitud_editar_evento.get_data())

        self.assertEqual(solicitud_editar_evento.status_code, 200)
        self.assertEqual(evento_editado["nombre_evento"], "Sakhir 130 vueltas")

    def test_obtener_evento_por_id(self):
        nuevo_evento = {
            "nombre": "GP de Miami",
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": 'Empate'
                }
            ],
            "tipo_evento": "MARCADOR"
        }

        endpoint_crear_evento = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_evento = self.client.post(endpoint_crear_evento,
                                                   data=json.dumps(nuevo_evento),
                                                   headers=headers)

        respuesta_al_crear_evento = json.loads(solicitud_nuevo_evento.get_data())
        id_evento = respuesta_al_crear_evento["id"]

        endpoint_obtener_evento = "/carrera/{}".format(str(id_evento))

        solicitud_consultar_evento_por_id = self.client.get(endpoint_obtener_evento, headers=headers)
        evento_obtenido = json.loads(solicitud_consultar_evento_por_id.get_data())

        self.assertEqual(solicitud_consultar_evento_por_id.status_code, 200)
        self.assertEqual(evento_obtenido["nombre_evento"], "GP de Miami")

    def test_obtener_eventos(self):
        nuevo_evento = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": 'Empate'
                }
            ],
            "tipo_evento": "MARCADOR"
        }

        endpoint = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_consultar_eventos_antes = self.client.get(endpoint, headers=headers)
        total_eventos_antes = len(json.loads(solicitud_consultar_eventos_antes.get_data()))

        solicitud_consultar_eventos_despues = self.client.post(endpoint,
                                                                data=json.dumps(nuevo_evento),
                                                                headers=headers)

        total_eventos_despues = len(json.loads(solicitud_consultar_eventos_despues.get_data()))

        self.assertEqual(solicitud_consultar_eventos_despues.status_code, 200)
        self.assertGreater(total_eventos_despues, total_eventos_antes)

    def test_eliminar_evento(self):
        nuevo_evento = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": 'Empate'
                }
             
            ],
            "tipo_evento": "MARCADOR"
        }

        endpoint_eventos = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_evento = self.client.post(endpoint_eventos,
                                                   data=json.dumps(nuevo_evento),
                                                   headers=headers)

        id_evento = json.loads(solicitud_nuevo_evento.get_data())["id"]
        solicitud_consultar_eventos_antes = self.client.get(endpoint_eventos, headers=headers)
        total_eventos_antes = len(json.loads(solicitud_consultar_eventos_antes.get_data()))

        endpoint_evento = "/carrera/{}".format(str(id_evento))

        solicitud_eliminar_evento = self.client.delete(endpoint_evento, headers=headers)
        solicitud_consultar_eventos_despues = self.client.get(endpoint_evento, headers=headers)
        total_eventos_despues = len(json.loads(solicitud_consultar_eventos_despues.get_data()))
        solicitud_consultar_evento_por_id = self.client.get(endpoint_evento, headers=headers)

        #self.assertLess(total_eventos_despues, total_eventos_antes)
        self.assertEqual(solicitud_consultar_evento_por_id.status_code, 404)
        self.assertEqual(solicitud_eliminar_evento.status_code, 204)
