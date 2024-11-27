from unittest import TestCase
import pandas as pd
from entities.slot import Slot
import datetime as datetime

class TestSlot(TestCase):
    def setUp(self):
        self.vuelos = pd.DataFrame.from_dict({
            'id': {0: 'VY4548', 1: 'VY3887', 2: 'VY1603', 3: 'VY3302', 4: 'VY1121'},
            'fecha_llegada': {0: '2022-08-06 10:30:00',
                              1: '2022-08-05 15:00:00',
                              2: '2022-08-05 08:45:00',
                              3: '2022-08-05 12:30:00',
                              4: '2022-08-06 10:15:00'},
            'retraso': {0: '00:10', 1: '00:10', 2: '-', 3: '00:15', 4: '-'},
            'tipo_vuelo': {0: 'NAT', 1: 'NAT', 2: 'INTERNAT', 3: 'NAT', 4: 'NAT'},
            'destino': {0: 'Helsinki', 1: 'Sevilla', 2: 'Nueva York', 3: 'Bruselas', 4: 'Paris'}
        })
        self.vuelos['fecha_llegada'] = pd.to_datetime(self.vuelos['fecha_llegada'])
        self.slot = Slot()
        self.slot.asigna_vuelo(
            'VY4548',
            datetime.datetime(2022, 8, 6, 10, 30, 0),
            datetime.datetime(2022, 8, 6, 11, 40, 0)
        )

    def test_slot_esta_libre_fecha_determinada(self):
        expected_time = datetime.timedelta(minutes=30)  
        d = datetime.datetime(2022, 8, 6, 11, 10, 0)   
        tmp = self.slot.slot_esta_libre_fecha_determinada(d)
        self.assertEqual(expected_time, tmp)           

        expected_time = datetime.timedelta(0)          
        d = datetime.datetime(2022, 8, 6, 11, 50, 0)   
        tmp = self.slot.slot_esta_libre_fecha_determinada(d)
        self.assertEqual(expected_time, tmp)          

import datetime as dt
class Slot:
    def __init__(self): 
        self.id = None
        self.fecha_inicial = None
        self.fecha_final = None

    def asigna_vuelo(self, id, fecha_llegada, fecha_despegue):
        self.id = id
        self.fecha_inicial = fecha_llegada
        self.fecha_final = fecha_despegue

    def slot_esta_libre_fecha_determinada(self, fecha): 
        time_to_wait = dt.timedelta(0)
        if self.fecha_final is not None:
            time_to_wait = max(self.fecha_final - fecha, dt.timedelta(0))
        return time_to_wait