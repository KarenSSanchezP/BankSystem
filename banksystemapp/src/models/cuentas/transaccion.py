# transaccion.py
from datetime import datetime

class Transaccion:
    def __init__(self, id_transaccion, id_cuenta, tipo, monto, fecha_hora=None):
        self.id_transaccion = id_transaccion
        self.id_cuenta = id_cuenta
        self.tipo = tipo
        self.monto = float(monto)
        self.fecha_hora = fecha_hora if fecha_hora else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):  # ✅ indentado dentro de la clase
        return f"[{self.fecha_hora}] {self.tipo}: ${self.monto:.2f} (Cuenta: {self.id_cuenta})"
    
    
# from datetime import datetime

# class Transaccion:
#     def __init__(self, id_transaccion, id_cuenta, tipo, monto, fecha_hora = None):
#         self.id_transaccion = id_transaccion
#         self.id_cuenta = id_cuenta
#         self.tipo = tipo
#         self.monto = monto
#         self.fecha_hora = fecha_hora if fecha_hora else datetime.now()
    
# def __str__(self):
#         return f"[{self.fecha_hora}] {self.tipo}: ${self.monto} (Cuenta: {self.id_cuenta})"