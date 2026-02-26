from .menu_base import MenuBase
from .menu_analitica import MenuAnalitica
from ..services.usuario_service import UsuarioService
from ..services.cuenta_service import CuentaService

class MenuAdmin(MenuBase):
    def __init__(self, usuario_logueado):
        super().__init__()
        self.usuario_service = UsuarioService()
        self.cuenta_service = CuentaService()
        self.menu_analitica = MenuAnalitica()
        self.usuario = usuario_logueado
        self.opciones = [
            '1. Crear cliente',
            '2. Crear cuenta a cliente',
            '3. Bloquear / activar cuenta',
            '4. Listar usuarios / cuentas',
            '5. Analisis de datos',
            '6. Salir'
        ]
    
    # =================================================================
    # -------- EJECUCION PRINCIPAL DEL MENÚ DE ADMINISTRADOR ----------
    # =================================================================
    def ejecutar(self):
        """
        Bucle principal del menu de administración
        """
        while True:
            self.mostrar_encabezado(f"Panel de administrador - {self.usuario.userName}", 44)
            
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
    
    # ===================================================================
    # - Métodos para las opciones de crear clientes y manejo de cuentas -
    # ===================================================================
    def crear_cliente(self):
        """
        Permite crear un nuevo cliente
        """
        self.mostrar_encabezado("Crear cliente", 35, simbolo="-", es_salto_de_linea=True)
        
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
            
            # Obtener el estado actual de la cuenta para mostrar la opción correspondiente
            cuentas = self.cuenta_service.listar_cuentas()
            cuenta = next((c for c in cuentas if c.id_cuenta == id_cuenta), None)
            
            if not cuenta:
                raise ValueError(f"No se encontró ninguna cuenta con el ID '{id_cuenta}'.")

            if cuenta.esta_activa():
                op = input("La cuenta está actualmente Activa. \nPresione 1 para bloquearla o 2 para cancelar... ")
                accion = 'bloquear' if op == '1' else None
            else:
                op = input("La cuenta está actualmente Bloqueada. \nPresione 1 para activarla o 2 para cancelar... ")
                accion = 'activar' if op == '1' else None
                
            if not accion:
                print("\nOperación cancelada.")
            else:
                # Llamar al servicio para alternar el estado de la cuenta
                exito, msg = self.cuenta_service.alternar_estado_cuenta(id_cuenta, accion)
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
        while True:
            self.mostrar_encabezado("Listar usuarios / cuentas", 40, simbolo="-", es_salto_de_linea=True)
            
            try:
                opciones = [
                    '1. Listar todos los clientes',
                    '2. Listar todos los administradores',
                    '3. Listar todas las cuentas',
                    '4. Regresar'
                ]
                for opcion in opciones:
                    print(f"\t{opcion}")
                
                seleccion = self.pedir_opcion(opciones)
                
                if seleccion == '1':
                    self.listar_todos_clientes()
                elif seleccion == '2':
                    self.listar_todos_administradores()
                elif seleccion == '3':
                    self.listar_todas_cuentas()
                elif seleccion == '4':
                    self.limpiar_consola()
                    break  # Solo regresa al menú principal
                else:
                    print("Opción no válida. Intente nuevamente")
                    self.pausa(2)
                    self.limpiar_consola()
            except Exception as e:
                print(f"Error: {e}")
                self.continuar()
                self.limpiar_consola()
    
    # =================================================================    
    # -------------- EJECUCIÓN DEL MODULO DE ANALITICA ----------------
    # =================================================================
    def ejecucion_modulo_analitica(self):
        """
        Permite ejecutar el módulo de análitica
        """
        self.menu_analitica.ejecutar()
    
    # =================================================================
    # ------- Métodos auxiliares para listar usuarios y cuentas -------
    # =================================================================
    def listar_todos_clientes(self):
        self.mostrar_encabezado("Clientes registrados", 40, simbolo="-", es_salto_de_linea=True)
        clientes = self.usuario_service.listar_clientes()
        
        if not clientes:
            print("No hay clientes registrados.")
        else:
            print(f"{'ID':<6} {'Username':<10} {'Nombres':<20} {'Apellidos':<20} {'DUI':<12}")
            print("-" * 70)
            for cl in clientes:
                print(f"{cl.userId:<6} {cl.userName:<10} {cl.nombres:<20} {cl.apellidos:<20} {cl.dui:<12}")
        
        self.continuar()
        self.limpiar_consola()

    def listar_todos_administradores(self):
        self.mostrar_encabezado("Administradores registrados", 40, simbolo="-", es_salto_de_linea=True)
        admins = self.usuario_service.listar_admins()
        
        if not admins:
            print("No hay administradores registrados.")
        else:
            print(f"{'ID':<6} {'Username':<10} {'Nombres':<20} {'Apellidos':<20} {'DUI':<12}")
            print("-" * 70)
            for a in admins:
                print(f"{a.userId:<6} {a.userName:<10} {a.nombres:<20} {a.apellidos:<20} {a.dui:<12}")
        
        self.continuar()
        self.limpiar_consola()

    def listar_todas_cuentas(self):
        self.mostrar_encabezado("Cuentas registradas", 40, simbolo="-", es_salto_de_linea=True)
        cuentas = self.cuenta_service.listar_cuentas()
        
        if not cuentas:
            print("No hay cuentas registradas.")
        else:
            print(f"{'ID':<8} {'DUI Propietario':<16} {'Tipo':<12} {'Saldo':>10}  {'Estado':<12}")
            print("-" * 60)
            for c in cuentas:
                print(f"{c.id_cuenta:<8} {c.dui_propietario:<16} {c.tipo:<12} ${c.saldo:>9.2f}  {c.estado:<12}")
        
        self.continuar()
        self.limpiar_consola()