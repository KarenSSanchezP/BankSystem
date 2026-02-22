class CuentaBancaria:
    def __init__(self, id_cuenta, dui_propietario, tipo, saldo, estado='Activa'):
        self._id_cuenta = id_cuenta
        self._dui_propietario = dui_propietario
        self._tipo = tipo
        self._saldo = float(saldo)
        self._estado = estado

    @property
    def id_cuenta(self):
        return self._id_cuenta

    @property
    def dui_propietario(self):
        return self._dui_propietario

    @property
    def tipo(self):
        return self._tipo

    @property
    def saldo(self):
        return self._saldo

    @property
    def estado(self):
        return self._estado

    def esta_activa(self):
        return self._estado == 'Activa'

    def depositar(self, monto):
        self._saldo += monto

    def retirar(self, monto):
        self._saldo -= monto

    def bloquear(self):
        self._estado = 'Bloqueada'

    def activar(self):
        self._estado = 'Activa'

    def __str__(self):
        return f"[{self._id_cuenta}] {self._tipo} | Saldo: ${self._saldo:.2f} | Estado: {self._estado}"
    
    
# from datetime import datetime

# class CuentaBancaria:
#     def __init__(self, id_cuenta, dui_propietario, tipo, saldo, estado):
#         self.id_cuenta = id_cuenta
#         self.dui_propietario = dui_propietario
#         self.tipo = tipo
#         self.saldo = float(saldo)
#         self.estado = estado