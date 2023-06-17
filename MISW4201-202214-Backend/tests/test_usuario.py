import json
from unittest import TestCase
from faker import Faker
from faker.generator import random

from app import app

class TestUsuario(TestCase):
    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
    
    def test_crear_usuario_vacio(self):
        nuevo_usuario = {
            "usuario": None,
            "nombre": None,
            "contrasena": None,
            "numero_tarjeta": None,
        }
        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        self.assertEqual(solicitud_nuevo_usuario.status_code,400)

    def test_crear_usuario_existente(self):
        nuevo_usuario = {
            "usuario": self.data_factory.email(),
            "nombre": self.data_factory.name(),
            "contrasena": self.data_factory.password(),
            "numero_tarjeta": str(self.data_factory.random_number(digits=16)),
        }

        solicitud_nuevo_usuario_1 = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})
        
        solicitud_nuevo_usuario_2 = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})
        
        self.assertEqual(solicitud_nuevo_usuario_1.status_code,200)
        self.assertEqual(solicitud_nuevo_usuario_2.status_code,400)

    def test_crear_usuario_con_valores_erroneos(self):
        nuevo_usuario = {
            "usuario": 1000,
            "nombre": True,
            "contrasena": self.data_factory.password(60),
            "numero_tarjeta": str(self.data_factory.random_number(digits=20)),
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})
        
        self.assertEqual(solicitud_nuevo_usuario.status_code,400)
        

    
