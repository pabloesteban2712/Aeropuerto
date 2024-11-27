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

    def slot_esta_libre_fecha_determinada(self, fecha): #debe calcular cuanto falta para que quede un slot libre
        time_to_wait = dt.timedelta (0)
        if self.fecha_final is not None:
            time_to_wait = max(self.fecha_final - fecha, dt.timedelta(0))
        return time_to_wait