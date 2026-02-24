from .menu_base import MenuBase
from .menu_admin import MenuAdmin
from .menu_cliente import MenuCliente
from ..services.auth_service import AuthService

class MenuPrincipal(MenuBase):
    def __init__(self):
        super().__init__()
        self.opciones = [
            '1. Iniciar sesión',
            '2. Salir'
        ]
        self.auth_service = AuthService()
    
    def ejecutar(self):
        """
        Bucle principal del menu principal
        """
        while True:
            self.mostrar_encabezado(" "*5 +"Banking System", 43)
            
            for opcion in self.opciones:
                print(f"\t{opcion}")
            
            try:
                seleccion = self.pedir_opcion(self.opciones)
                
                if seleccion == '1':
                    self.iniciar_sesion()
                elif seleccion == '2':
                    self.salir("Cerrando el sistema...")
                    break
                else:
                    print("Opción no válida. Intente nuevamente")
                    self.pausa(2)
                    self.limpiar_consola()
            except Exception as e:
                print(f"Error: {e}")
                self.pausa(2)
                self.limpiar_consola()
    
    def iniciar_sesion(self):
        """
        Permite iniciar sesión en el sistema
        """
        self.mostrar_encabezado(" "*4+"Iniciar sesión", 40, simbolo="-", es_salto_de_linea=True)
        
        try:
            opciones_inicio = [
                '1. Administrador',
                '2. Cliente',
                '3. Regresar al menú principal'
            ]
            for opcion in opciones_inicio:
                print(f"\t{opcion}")
            seleccion = self.pedir_opcion(opciones_inicio)
            
            if seleccion == '1':
                self.mostrar_encabezado("Iniciar sesión como administrador", 50, simbolo="-", es_salto_de_linea=True)
                print("Escriba '0' en el nombre de usuario para salir del inicio de sesión")
                username_input = input(">>> Nombre de usuario (ej.: AA1): ")
                
                if username_input == '0':
                    self.limpiar_consola()
                    return
                usuario_logueado = self.auth_service.login_admin(username_input)
                print(f"\n\t--- Bienvenido {usuario_logueado.userName}! ---")
                self.pausa(2)
                
                self.redirigir_por_rol(usuario_logueado)
                
            elif seleccion == '2':
                self.mostrar_encabezado("Iniciar sesión como cliente", 45, simbolo="-", es_salto_de_linea=True)
                print("Escriba '0' en su DUI para salir del inicio de sesión")
                
                dui_input = input(">>> DUI (ej.: 01234567-1): ")
                if dui_input == '0':
                    self.limpiar_consola()
                    return
                pin_input = input(">>> PIN (4 digitos): ")  
                
                usuario_logueado = self.auth_service.login_cliente(dui_input, pin_input)
                print(f"\n\t--- Bienvenido {usuario_logueado.userName}! ---")
                self.pausa(2)
                
                self.redirigir_por_rol(usuario_logueado)
            elif seleccion == '3':
                self.salir("Volviendo al menú principal...")
            else:
                print("Opción no válida. Intente nuevamente")
                self.pausa(2)
                self.limpiar_consola()
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            self.pausa(2)
            self.limpiar_consola()
    
    def redirigir_por_rol(self, usuario):
        """
        Permite redireccionar al menu de administrador o cliente 
        dependiendo del rol del usuario
        """
        if usuario.rol == 'Admin':
            menu_admin = MenuAdmin(usuario)
            menu_admin.ejecutar()
        elif usuario.rol == 'Cliente':
            menu_cliente = MenuCliente(usuario)
            menu_cliente.ejecutar()
        else:
            print("Usuario no válido. Intente nuevamente")
            self.pausa(2)
            self.limpiar_consola()
    