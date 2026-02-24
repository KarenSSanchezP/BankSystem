from .menu_base import MenuBase

class MenuCliente(MenuBase):
    def __init__(self, usuario_logueado):
        super().__init__()
        self.usuario = usuario_logueado
        self.opciones = [
            '1. Saldo de sus cuentas',
            '2. Historial de movimientos',
            '3. Depositar',
            '4. Retirar',
            '5. Transferir entre cuentas',
            '6. Cerrar sesion'
        ]
    
    def ejecutar(self):
        """
        Bucle principal del menu de cliente
        """
        while True:
            self.mostrar_encabezado(f"Panel de cliente - {self.usuario.userName}", 40)
            
            for opcion in self.opciones:
                print(f"\t{opcion}")
            
            seleccion = self.pedir_opcion(self.opciones)
            
            if seleccion == '1':
                self.saldo_cuentas()
            elif seleccion == '2':
                self.historial_movimientos()
            elif seleccion == '3':
                self.depositar()
            elif seleccion == '4':
                self.retirar()
            elif seleccion == '5':
                self.transferir_entre_cuentas()
            elif seleccion == '6':
                self.salir("Cerrando sesión del cliente...")
                break
            else:
                print("Opción no válida. Intente nuevamente")
                self.pausa(2)
                self.limpiar_consola()
    
    def saldo_cuentas(self):
        """
        Permite ver el saldo de las cuentas del cliente
        """
        self.mostrar_encabezado("Saldo de sus cuentas", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def historial_movimientos(self):
        """
        Permite ver el historial de movimientos del cliente
        """
        self.mostrar_encabezado("Historial de movimientos", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def depositar(self):
        """
        Permite depositar dinero en una cuenta
        """
        self.mostrar_encabezado("Depositar", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def retirar(self):
        """
        Permite retirar dinero de una cuenta
        """
        self.mostrar_encabezado("Retirar", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def transferir_entre_cuentas(self):
        """
        Permite transferir dinero entre cuentas
        """
        self.mostrar_encabezado("Transferir entre cuentas", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()