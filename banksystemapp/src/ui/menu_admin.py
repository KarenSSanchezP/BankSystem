from .menu_base import MenuBase
from ..services.usuario_services import UsuarioService
from ..services.cuenta_service import CuentaService

class MenuAdmin(MenuBase):
    def __init__(self, usuario_logueado):
        super().__init__()
        self.usuario_service = UsuarioService()
        self.cuenta_service = CuentaService()
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
        
        try:
            lista_datos_cliente = []
            for dato in ['nombres', 'apellidos', 'DUI', 'contraseña (PIN)']:
                dato = input(f"Ingrese {dato}: ")
                if not dato:
                    raise ValueError("Todos los campos son obligatorios.")
                lista_datos_cliente.append(dato)
            
            if len(lista_datos_cliente[3]) != 4:
                raise ValueError("La contraseña debe tener 4 caracteres.")
            
            msg = self.usuario_service.crear_cliente(*lista_datos_cliente)
            print(msg)
            self.continuar()
            self.limpiar_consola()
        except ValueError as e:
            print(f"Error: {e}")
            self.continuar()
            self.limpiar_consola()
    
    def crear_cuenta_a_cliente(self):
        """
        Permite crear una nueva cuenta a un cliente
        """
        self.mostrar_encabezado("Crear cuenta a cliente", 40, simbolo="-", es_salto_de_linea=True)
        
        try:
            dui_propietario = input("Ingrese el DUI del cliente: ")
            if not dui_propietario:
                raise ValueError("El DUI es obligatorio.")
                
            # Validar que el cliente exista
            exito, cliente = self.usuario_service.obtener_cliente(dui_propietario)
            if not exito:
                raise ValueError("No existe un cliente registrado con ese DUI.")

            tipo = input("Ingrese el tipo de cuenta (Ahorro/Corriente): ").capitalize()
            if tipo not in ['Ahorro', 'Corriente']:
                raise ValueError("El tipo de cuenta debe ser 'Ahorro' o 'Corriente'.")

            saldo_str = input("Ingrese el saldo inicial: ")
            try:
                saldo = float(saldo_str)
                if saldo < 0:
                    raise ValueError("El saldo inicial no puede ser negativo.")
            except ValueError:
                raise ValueError("El saldo debe ser un valor numérico válido.")
            
            # Llamar al servicio para crear la cuenta
            exito, msg = self.cuenta_service.crear_cuenta(dui_propietario, tipo, saldo)
            print(msg)
            
            self.continuar()
            self.limpiar_consola()
        except ValueError as e:
            print(f"Error: {e}")
            self.continuar()
            self.limpiar_consola()
    
    def bloquear_activar_cuenta(self):
        """
        Permite bloquear o activar una cuenta
        """
        self.mostrar_encabezado("Bloquear / activar cuenta", 40, simbolo="-", es_salto_de_linea=True)
        
        try:
            id_cuenta = input("Ingrese el ID de la cuenta (ej. C001): ").strip()
            if not id_cuenta:
                raise ValueError("El ID de la cuenta es obligatorio.")
            
            # Llamar al servicio para alternar el estado de la cuenta
            exito, msg = self.cuenta_service.alternar_estado_cuenta(id_cuenta)
            print(msg)
            self.continuar()
            self.limpiar_consola()
        except ValueError as e:
            print(f"Error: {e}")
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