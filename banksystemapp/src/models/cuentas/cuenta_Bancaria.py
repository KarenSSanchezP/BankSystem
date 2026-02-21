from datetime import datetime

class CuentaBancaria:
    def __init__(self, id_cuenta, dui_propietario, tipo, saldo, estado):
        self.id_cuenta = id_cuenta
        self.dui_propietario = dui_propietario
        self.tipo = tipo
        self.saldo = float(saldo)
        self.estado = estado