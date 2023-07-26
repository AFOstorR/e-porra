import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app


class TestTransferirDinero(TestCase):

    def setUp(self):

        self.data_factory = Faker()
        self.client = app.test_client()

        '''Crear usuarios apostadores'''
        self.usuarios = list()

        for i in range(3):
            usuario = {
                    "usuario": self.data_factory.email(),
                    "nombre": self.data_factory.name(),
                    "contrasena": self.data_factory.password(),
                    "numero_tarjeta": str(self.data_factory.random_number(digits=16)),
                    "es_apostador": i < 2
                }
            solicitud_nuevo_usuario = self.client.post("/signin",
                                                    data = json.dumps(usuario),
                                                    headers = {'Content-Type': 'application/json'})

            respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
            self.usuarios.append(respuesta_al_crear_usuario)
        
        '''Crear carrera'''
        carrera = {
            "nombre": self.data_factory.word().capitalize() + ' ' + self.data_factory.city(),
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
                    "competidor": self.data_factory.name()
                }
            ],
            "tipo_evento": "CARRERA"
        }

        endpoint_crear_carrera = "/usuario/{}/carreras".format(str(self.usuarios[-1]['id']))
        self.headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.usuarios[-1]['token'])}

        solicitud_nueva_carrera = self.client.post(endpoint_crear_carrera,
                                                     data = json.dumps(carrera),
                                                     headers = self.headers)
        respuesta_al_crear_carrera = json.loads(solicitud_nueva_carrera.get_data())
        self.carrera = respuesta_al_crear_carrera

        '''Crear apuestas'''
        self.apuestas = list()
        for i in range(2):
            apuesta = {
                        "valor_apostado": random.uniform(100, 500000),
                        "nombre_apostador": self.usuarios[i]['usuario']['nombre'],
                        "id_competidor": self.carrera['competidores'][i]['id'],
                        "id_evento": self.carrera['id']
                    }
            endpoint_apuestas = "/apuestas/{}".format(str(self.usuarios[i]['id']))
            solicitud_nueva_apuesta = self.client.post(endpoint_apuestas,
                                                   data=json.dumps(apuesta),
                                                   headers = self.headers)
            respuesta_al_crear_apuesta = json.loads(solicitud_nueva_apuesta.get_data())
            self.apuestas.append(respuesta_al_crear_apuesta)

    def test_transferir_dinero_ganadores(self):
        endpoint_terminacion = '/carrera/{}/terminacion'.format(self.carrera['competidores'][0]['id'])
        solicitud_terminacion = self.client.put(endpoint_terminacion)
        endpoint_transacciones = '/transaccion/{}'.format(self.usuarios[0]['id'])
        solicitud_transacciones = self.client.get(endpoint_transacciones, headers = self.headers)
        transacciones = json.loads(solicitud_transacciones.get_data())
        self.assertIsNotNone(transacciones)
        self.assertGreater(len(transacciones), 0)
        self.assertEqual([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['tipo_transaccion'], 'GANANCIA')
        #self.assertEqual(round([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['valor'], 2), 
        #    round(float(self.apuestas[0]['valor_apostado'])* (1 + 1/round(float(self.carrera['competidores'][0]["probabilidad"])/ (1.0 - float(self.carrera['competidores'][0]["probabilidad"])), 2)),2))
        
    def test_retiro_dinero_casa(self):
        endpoint_terminacion = '/carrera/{}/terminacion'.format(self.carrera['competidores'][0]['id'])
        self.client.put(endpoint_terminacion)
        endpoint_transacciones = '/transaccion/{}'.format(self.usuarios[-1]['id'])
        solicitud_transacciones = self.client.get(endpoint_transacciones, headers = self.headers)
        transacciones = json.loads(solicitud_transacciones.get_data())
        self.assertIsNotNone(transacciones)
        self.assertGreater(len(transacciones), 0)
        self.assertEqual([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['tipo_transaccion'], 'GANANCIA')
        #self.assertEqual(round([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['valor'], 2), 
        #    -round(float(self.apuestas[0]['valor_apostado'])* (1 + 1/round(float(self.carrera['competidores'][0]["probabilidad"])/ (1.0 - float(self.carrera['competidores'][0]["probabilidad"])), 2)),2))

    def test_mensaje_ganador(self):
        endpoint_terminacion = '/carrera/{}/terminacion'.format(self.carrera['competidores'][0]['id'])
        self.client.put(endpoint_terminacion)
        endpoint_transacciones = '/transaccion/{}'.format(self.usuarios[0]['id'])
        solicitud_transacciones = self.client.get(endpoint_transacciones, headers = self.headers)
        transacciones = json.loads(solicitud_transacciones.get_data())
        self.assertIsNotNone(transacciones)
        self.assertGreater(len(transacciones), 0)
        self.assertEqual([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['descripcion'], 
            'Felicitaciones! Has ganado $ {:,.2f}  por tu apuesta en {}'.format(
                round([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['valor'], 2),
                self.carrera['nombre_evento']
                )
            )

    def test_mensaje_perdedor(self):
        endpoint_terminacion = '/carrera/{}/terminacion'.format(self.carrera['competidores'][0]['id'])
        self.client.put(endpoint_terminacion)
        endpoint_transacciones = '/transaccion/{}'.format(self.usuarios[1]['id'])
        solicitud_transacciones = self.client.get(endpoint_transacciones, headers = self.headers)
        transacciones = json.loads(solicitud_transacciones.get_data())
        self.assertIsNotNone(transacciones)
        self.assertGreater(len(transacciones), 0)
        self.assertEqual([transaccion for transaccion in transacciones if transaccion['fecha'] == max([transaccion['fecha'] for transaccion in transacciones])][0]['descripcion'], 
            'El evento {} ha finalizado. Tu ganancia fue $0.00'.format(self.carrera['nombre_evento'])
        )
