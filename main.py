import os
import pandas as pd

from entities.aeropuerto import aeropuerto
from entities.lector import LectorTXT, LectorCSV, LectorJSON
from entities.slot import Slot

def preprocess_data(df_list):
    df_= pd.concat (df_list) #Concatena los 3 dataframes, en 1 
    df_['fecha_llegada'] = df_['fecha_llegada'].apply(lambda x: x.replace ('T', ' '))
    df_['fecha_llegada'] = pd.to_datetime (df_['fecha_llegada'])
    return df_


if __name__ == '__main__': #Esto es lo que se va a ejecutarse, en caso de llamada
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')

    lectortxt = LectorTXT (path_1)
    lectorcsv = LectorCSV (path_2)
    lectorjson = LectorJSON (path_3)

    d_txt = lectortxt.lee_archivo()
    df_text = lectortxt.convierte_dict_a_csv(d_txt)
    
    df_csv = lectorcsv.lee_archivo()

    d_json = lectorjson.lee_archivo()
    df_json = lectorjson.convierte_dict_a_csv(d_json)

    df = preprocess_data ([df_text, df_csv, df_json])

    aeropuerto = aeropuerto (vuelos = df, slots = 3, t_embarque_nat= 60,  t_embarque_nat= 60 )
    aeropuerto.asigna_slots()