import pandas as pd #Vers
import datetime as dt
from entities.slot import Slot

class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        """
        Calcula la fecha de despegue a partir de la fecha de llegada y el retraso.
        Si el vuelo es internacional, se añade un tiempo de embarque más largo.
        """
        time_offset = self.tiempo_embarque_nat
        if row['tipo_vuelo'] == 'INTERNAT':
            time_offset = self.tiempo_embarque_internat

        retraso = 0
        if row['retraso'] != '-':
            tmp = pd.to_datetime(row['retraso'], format='%H:%M').time()
            retraso = tmp.minute * 60 + tmp.second

        row['fecha_despegue'] = row['fecha_llegada'] + pd.Timedelta(minutes=time_offset) + pd.Timedelta(seconds=retraso)
        return row

    def encuentra_slot(self, fecha_vuelo) -> int:
        """
        Busca un slot disponible para la fecha de vuelo dada.
        Retorna el ID del slot si está disponible, -1 si no.
        """
        for id, slot in self.slots.items():
            time_to_wait = slot.slot_esta_libre_fecha_determinada(fecha_vuelo)
            if time_to_wait.total_seconds() == 0:
                return id 

        return -1 

    def asigna_slot(self, vuelo) -> pd.Series:
        """
        Asigna un slot a un vuelo, calculando la fecha de despegue.
        Si no hay un slot disponible, se reintenta hasta encontrar uno.
        """
        slot = -1
        fecha_vuelo_original = vuelo['fecha_llegada']
        fecha_vuelo = fecha_vuelo_original

        while slot == -1:
            slot = self.encuentra_slot(fecha_vuelo)
            if slot == -1:
                fecha_vuelo += dt.timedelta(minutes=10)

       
        vuelo = self.calcula_fecha_despegue(vuelo)
        vuelo['fecha_llegada'] = fecha_vuelo  

        self.slots[slot].asigna_vuelo(vuelo['id'], vuelo['fecha_llegada'], vuelo['fecha_despegue'])
        vuelo['slot'] = slot

        return vuelo

    def asigna_slots(self):
        """
        Asigna slots a todos los vuelos en el DataFrame, respetando el orden de llegada.
        Si no hay un slot disponible, se pospone el vuelo.
        """
        self.df_vuelos.sort_values(by=['fecha_llegada'], inplace=True)
        
        while len(self.df_vuelos) > 0:
            df_i = self.df_vuelos.iloc[0:self.n_slots, :]
            df_i = df_i.apply(lambda vuelo: self.asigna_slot(vuelo), axis=1)

            self.df_vuelos = self.df_vuelos.iloc[self.n_slots:, :]