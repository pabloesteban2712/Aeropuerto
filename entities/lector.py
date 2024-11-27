import json
import os
import pandas as pd

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension: str) -> bool:
        file_extension = os.path.splitext(self.path)[1]
        if extension != file_extension:
            raise ValueError("El archivo no tiene la extensión adecuada.")
        return True

    def lee_archivo(self):
        pass

    @staticmethod
    def convierte_dict_a_csv(list_dicts: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(list_dicts)
        return df

class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self, datetime_columns=None) -> pd.DataFrame:
        df = None
        try:
            if super()._comprueba_extension('.csv'):
                df = pd.read_csv(self.path)
                if datetime_columns:
                    for col in datetime_columns:
                        df[col] = pd.to_datetime(df[col])
        except FileNotFoundError:
            print(f"El archivo {self.path} no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
        return df

class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        list_vuelos = []
        try:
            if super()._comprueba_extension('.json'):
                with open(self.path, "r", encoding="utf-8") as file:
                    list_vuelos = json.load(file)
                    if not isinstance(list_vuelos, list) or not all(isinstance(d, dict) for d in list_vuelos):
                        raise ValueError("El archivo JSON no contiene una lista de diccionarios.")
        except FileNotFoundError:
            print(f"El archivo {self.path} no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
        return list_vuelos

class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        
    def lee_archivo(self):
        if super()._comprueba_extension('.txt'):
            with open(self.path, 'r', encoding='utf-8') as file:
                cabecera = file.readline().strip().split(",")
                data = []
                for linea in file:
                    valores = [valor.strip() for valor in linea.strip().split(",")]
                    
                    if len(valores) == len(cabecera):
                        registro = {cabecera[i].strip(): valores[i] for i in range(len(cabecera))}
                        data.append(registro)
                    else:
                        print(f"Línea ignorada (mal formada o con valores extras): {