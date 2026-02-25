from datetime import datetime

class Transferencia:
    def __init__(self, id_transferencia, id_origen, id_destino, monto, fecha_hora = None):
        self.id_transferencia = id_transferencia
        self.id_origen = id_origen  
        self.id_destino = id_destino
        self.monto = monto
        self.fecha_hora = fecha_hora if fecha_hora else datetime.now()
        
    def __str__(self):
        return f"[{self.fecha_hora}] TRANSFERENCIA: ${self.monto} | {self.id_origen} -> {self.id_destino}"