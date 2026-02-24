from .menu_base import MenuBase

class MenuAdmin(MenuBase):
    def __init__(self, usuario_logueado):
        super().__init__()
        self.usuario = usuario_logueado
        self.opciones = [
            '1. Crear cliente',
            '2. Crear cuenta a cliente',
            '3. Bloquear / activar cuenta',
            '4. Listar usuarios / cuentas',
            '5. Ejecucion de modulo de analitica',
            '6. Salir'
        ]
    
    def ejecutar(self):
        """
        Bucle principal del menu de administración
        """
        while True:
            self.mostrar_encabezado(f"Panel de administrador - {self.usuario.userName}", 40)
            
            for opcion in self.opciones:
                print(f"\t{opcion}")
            
            seleccion = self.pedir_opcion(self.opciones)
            
            if seleccion == '1':
                self.crear_cliente()
            elif seleccion == '2':
                self.crear_cuenta_a_cliente()
            elif seleccion == '3':
                self.bloquear_activar_cuenta()
            elif seleccion == '4':
                self.listar_usuarios_cuentas()
            elif seleccion == '5':
                self.ejecucion_modulo_analitica()
            elif seleccion == '6':
                self.salir("Cerrando sesión del administrador...")
                break
            else:
                print("Opción no válida. Intente nuevamente")
                self.pausa(2)
                self.limpiar_consola()
    
    def crear_cliente(self):
        """
        Permite crear un nuevo cliente
        """
        self.mostrar_encabezado("Crear cliente", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def crear_cuenta_a_cliente(self):
        """
        Permite crear una nueva cuenta a un cliente
        """
        self.mostrar_encabezado("Crear cuenta a cliente", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def bloquear_activar_cuenta(self):
        """
        Permite bloquear o activar una cuenta
        """
        self.mostrar_encabezado("Bloquear / activar cuenta", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def listar_usuarios_cuentas(self):
        """
        Permite listar los usuarios y las cuentas
        """
        self.mostrar_encabezado("Listar usuarios / cuentas", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def ejecucion_modulo_analitica(self):
        """
        Permite ejecutar el módulo de análitica
        """
        self.mostrar_encabezado("Ejecución de modulo de análitica", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()