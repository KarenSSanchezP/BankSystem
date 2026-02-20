class Usuario():
    def __init__(self,nombres,apellidos,DUI,password,userName):
        self.nombres=nombres
        self.apellidos=apellidos
        self.dui=DUI
        self.password=password

class Administrador(Usuario):
    def __init__(self, nombres, apellidos, DUI, password, userName):
        super().__init__(nombres, apellidos, DUI, password, userName)

class Cliente(Usuario):
    def __init__(self, nombres, apellidos, DUI, password, userName):
        super().__init__(nombres, apellidos, DUI, password, userName)

class CuentaBancaria():
    def __init__(self,propietario,tipo,saldo,estado):
        self.propietario=propietario
        self.tipo=tipo
        self.saldo=saldo
        self.estado=estado
        pass


#Aqui tengo la duda si se hace una clase tanto para ceunta de ahorro como corriente