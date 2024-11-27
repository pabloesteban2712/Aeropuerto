from unittest import TestCase 
import pandas as pd
from pandas._testing import assert_series_equal
from entities.aeropuerto import Aeropuerto

class TestAeropuerto(TestCase):
    def setUp(self):
        vuelos = pd.DataFrame.from_dict({
            'id': {0: 'VY4548', 1: 'VY3887', 2: 'VY1603', 3: 'VY3302', 4: 'VY1121'},
            'fecha_llegada': {0: '2022-08-06 10:30:00',
                              1: '2022-08-05 09:00:00',
                              2: '2022-08-05 08:45:00',
                              3: '2022-08-05 08:30:00',
                              4: '2022-08-06 10:15:00'},
            'retraso': {0: '00:10', 1: '00:10', 2: '-', 3: '00:15', 4: '-'},
            'tipo_vuelo': {0: 'NAT', 1: 'NAT', 2: 'INTERNAT', 3: 'NAT', 4: 'NAT'},
            'destino': {0: 'Helsinki', 1: 'Sevilla', 2: 'Nueva York', 3: 'Bruselas', 4: 'Paris'}
        })
        vuelos['fecha_llegada'] = pd.to_datetime(vuelos['fecha_llegada'])
        n_slots = 2
        t_embarque_nat = 60
        t_embarque_internat = 100
        self.aeropuerto = Aeropuerto(vuelos, n_slots, t_embarque_nat, t_embarque_internat)

    def test_calcula_fecha_despegue(self):
        expected_fecha_llegada = pd.to_datetime('2022-08-06 11:50:00')
        expected_fecha_despegue = pd.to_datetime('2022-08-06 13:00:00')
        expected_vuelo = pd.Series({
            'id': 'VY4548', 
            'fecha_llegada': expected_fecha_llegada,
            'retraso': '00:10',
            'tipo_vuelo': 'NAT', 
            'destino': 'Helsinki',
            'fecha_despegue': expected_fecha_despegue,
            'slot': 1
        })
        vuelo = self.aeropuerto.calcula_fecha_despegue(expected_vuelo)
        assert_series_equal(expected_vuelo, vuelo, check_index=False)

    def test_encuentra_slot(self):
        expected_slot = 1
        row = self.aeropuerto.df_vuelos.iloc[0, :]
        slot = self.aeropuerto.encuentra_slot(row['fecha_llegada'])
        self.assertEqual(expected_slot, slot)

        self.aeropuerto.slots[1].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))
        self.aeropuerto.slots[2].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))

        expected_slot = -1
        row_2 = row.copy()
        row_2['fecha_llegada'] = row['fecha_llegada'] + pd.Timedelta(minutes=30)
        slot = self.aeropuerto.encuentra_slot(row_2['fecha_llegada'])
        self.assertEqual(expected_slot, slot)

        # Liberamos los slots para comprobar de nuevo
        self.aeropuerto.slots[1].fecha_inicial = None
        self.aeropuerto.slots[1].fecha_final = None
        self.aeropuerto.slots[2].fecha_inicial = None
        self.aeropuerto.slots[2].fecha_final = None

        expected_slot = 1  # Después de liberar, debería encontrar el primer slot disponible
        slot = self.aeropuerto.encuentra_slot(row_2['fecha_llegada'])
        self.assertEqual(expected_slot, slot)

    def test_asigna_slot(self):
        expected_fecha_llegada = pd.to_datetime('2022-08-06 11:50:00')
        expected_fecha_despegue = pd.to_datetime('2022-08-06 13:00:00')
        expected_vuelo = pd.Series({
            'id': 'VY4548', 
            'fecha_llegada': expected_fecha_llegada,
            'retraso': '00:10',
            'tipo_vuelo': 'NAT', 
            'destino': 'Helsinki',
            'fecha_despegue': expected_fecha_despegue,
            'slot': 1
        })

        row = self.aeropuerto.df_vuelos.iloc[0, :]
        self.aeropuerto.slots[1].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))
        self.aeropuerto.slots[2].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))

        row_2 = row.copy()
        row_2['fecha_llegada'] = row['fecha_llegada'] + pd.Timedelta(minutes=30)
        row_2 = self.aeropuerto.asigna_slot(row_2)

        expected_vuelo.name = 0
        assert_series_equal(expected_vuelo, row_2, check_index=False)