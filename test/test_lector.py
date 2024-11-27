from unittest import TestCase
import os
import pandas as pd
from pandas._testing import assert_frame_equal

from entities.lector import LectorCSV, LectorJSON, LectorTXT

class TestLector(TestCase):
    def test_lee_archivo_csv(self):
        path = os.path.abspath(r'C:\Users\poulv\Desktop\PYTHON\python_practica_a_completar\data\vuelos_2.csv')
        expected_df = pd.DataFrame([{'id': 'VY4548', 'fecha_llegada': '08/06/2022 10:30', 'retraso': '-',
                                     'tipo_vuelo': 'NAT', 'destino': 'Helsinki'},
                                    {'id': 'VY3888', 'fecha_llegada': '08/06/2022 15:00', 'retraso': '00:10',
                                     'tipo_vuelo': 'NAT', 'destino': 'Roma'},
                                    {'id': 'VY1605', 'fecha_llegada': '08/06/2022 08:45', 'retraso': '-',
                                     'tipo_vuelo': 'NAT', 'destino': 'Madrid'},
                                    {'id': 'VY3307', 'fecha_llegada': '08/05/2022 12:30', 'retraso': '-',
                                     'tipo_vuelo': 'INTERNAT', 'destino': 'Sao Paulo'}])
        expected_df['fecha_llegada'] = pd.to_datetime(expected_df['fecha_llegada'])
        lector = LectorCSV(path)
        df = lector.lee_archivo(datetime_columns=['fecha_llegada'])
        assert_frame_equal(expected_df, df)

    def test_lee_archivo_json(self):
        path = os.path.abspath(r'C:\Users\poulv\Desktop\PYTHON\python_practica_a_completar\data\vuelos_3.json')
        expected_list = [{'id': 'VY1606', 'fecha_llegada': '08/05/2022 11:15', 'retraso': '-', 'tipo_vuelo': 'INTERNAT',
                          'destino': 'Beijing'},
                         {'id': 'VY2650', 'fecha_llegada': '08/05/2022 20:30', 'retraso': '00:05', 'tipo_vuelo': 'NAT',
                          'destino': 'Marrakech'},
                         {'id': 'VY1415', 'fecha_llegada': '08/05/2022 12:10', 'retraso': '-', 'tipo_vuelo': 'NAT',
                          'destino': 'Florencia'},
                         {'id': 'VY6611', 'fecha_llegada': '08/05/2022 13:45', 'retraso': '-', 'tipo_vuelo': 'NAT',
                          'destino': 'Lisboa'}]
        lector = LectorJSON(path)
        d = lector.lee_archivo()
        self.assertListEqual(expected_list, d)

    def test_lee_archivo_txt(self):
        path = os.path.abspath(r'C:\Users\poulv\Desktop\PYTHON\python_practica_a_completar\data\vuelos_1.txt')
        expected_list = [
            {'id': 'VY4547', 'fecha_llegada': '08/05/2022T10:30', 'retraso': '-', 'tipo_vuelo': 'NAT',
             'destino': 'Paris'},
            {'id': 'VY3887', 'fecha_llegada': '08/05/2022T15:00', 'retraso': '00:10', 'tipo_vuelo': 'NAT',
             'destino': 'Sevilla'},
            {'id': 'VY1603', 'fecha_llegada': '08/05/2022T08:45', 'retraso': '-', 'tipo_vuelo': 'INTERNAT',
             'destino': 'Nueva York'},
            {'id': 'VY3302', 'fecha_llegada': '08/05/2022T12:30', 'retraso': '00:15', 'tipo_vuelo': 'NAT',
             'destino': 'Bruselas'}]
        lector = LectorTXT(path)
        d = lector.lee_archivo()
        self.assertListEqual(expected_list, d)

    def test_convierte_dict_a_csv(self):
        path = os.path.abspath(r'C:\Users\poulv\Desktop\PYTHON\python_practica_a_completar\data\vuelos_1.txt')
        lector = LectorTXT(path)
        d_1 = lector.lee_archivo()
        df_1 = lector.convierte_dict_a_csv(d_1)
        self.assertIsInstance(df_1, pd.DataFrame)

        path = os.path.abspath(r'C:\Users\poulv\Desktop\PYTHON\python_practica_a_completar\data\vuelos_3.json')
        lector = LectorJSON(path)
        d_2 = lector.lee_archivo()
        df_2 = lector.convierte_dict_a_csv(d_2)
        self.assertIsInstance(df_2, pd.DataFrame)