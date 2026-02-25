from datetime import datetime

class CuentaBancaria:
    def __init__(self, id_cuenta, dui_propietario, tipo, saldo, estado):
        self.id_cuenta = id_cuenta
        self.dui_propietario = dui_propietario
        self.tipo = tipo
        self.saldo = float(saldo)
        self.estado = estado

    def __str__(self):
        return f"Cuenta: {self.id_cuenta} | Tipo: {self.tipo} | Saldo: ${self.saldo:.2f} | Estado: {self.estado}"