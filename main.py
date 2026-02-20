from clases import Administrador,Cliente,CuentaBancaria

def menuCliente(usuario):
    while True:
        print("++++++++++ ROL CLIENTE ++++++++++")
        print("1. Saldo de sus cuentas")
        print("2. Historial de movimientos")
        print("3. Depositar")
        print("4. Retirar")
        print("5. Transferir entre cuentas")
        print("6. Cerrar sesion")



def  menuAdministrador(usuario,cuentabancaria):
    while True:
        print("++++++++++ ROL Administrador ++++++++++")
        print("1. Crear cliente")
        print("2. Crear cuenta a cliente")
        print("3. Bloquear / activar cuenta")
        print("4. Listar usuarios / cuentas")
        print("5. Ejecusion de modulo de analitica")
        print("6. Salir")
