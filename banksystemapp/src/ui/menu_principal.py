from .menu_base import MenuBase
from .menu_admin import MenuAdmin
from .menu_cliente import MenuCliente

class MenuPrincipal(MenuBase):
    def __init__(self):
        super().__init__()
        self.opciones = [
            '1. Iniciar sesión',
            '2. Salir'
        ]
    
    def ejecutar(self):
        """
        Bucle principal del menu principal
        """
        while True:
            self.mostrar_encabezado("Banking System", 40)
            
            for opcion in self.opciones:
                print(f"\t{opcion}")
            
            try:
                seleccion = self.pedir_opcion(self.opciones)
                
                if seleccion == '1':
                    self.iniciar_sesion()
                elif seleccion == '2':
                    self.salir("Cerrando sesión...")
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
        self.mostrar_encabezado("Iniciar sesión", 40, simbolo="-", es_salto_de_linea=True)
        
        try:
            opciones_inicio = [
                '1. Administrador',
                '2. Cliente'
            ]
            for opcion in opciones_inicio:
                print(f"\t{opcion}")
            seleccion = self.pedir_opcion(opciones_inicio)
            
            if seleccion == '1':
                print("Escriba '0' en el nombre de usuario para salir del inicio de sesión")
                username_input = input("Escriba el nombre de usuario: ")
                
                if username_input == '0':
                    self.limpiar_consola()
                    return
                usuario_logueado = self.auth_service.login_admin(username_input)
                print(f"\n\t--- Bienvenido {usuario_logueado.username}! ---")
                self.pausa(2)
                
                menu_admin = MenuAdmin(usuario_logueado)
                menu_admin.ejecutar()
                
            elif seleccion == '2':
                print("Escriba '0' en su DUI para salir del inicio de sesión")
                dui_input = input("Escriba su DUI : ")
                if dui_input == '0':
                    self.limpiar_consola()
                    return
                pin_input = input("Escriba su PIN: ")
                
                usuario_logueado = self.auth_service.login_cliente(dui_input, pin_input)
                print(f"\n\t--- Bienvenido {usuario_logueado.username}! ---")
                self.pausa(2)
                
                menu_cliente = MenuCliente(usuario_logueado)
                menu_cliente.ejecutar()
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
    
    