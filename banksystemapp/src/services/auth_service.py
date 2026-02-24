from ..repositories.usuarios.repositorioUsuario import UsuarioRepository
from ..models.usuarios.cliente import Cliente
from ..models.usuarios.admin import Administrador

class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()
    
    def login_admin(self, username):
        """
        Verificar credenciales de un administrador
        """
        try:
            usuario = self.repo.obtener_usuario_por_username(username)
            if usuario.rol == 'Admin':
                return usuario
            else:
                raise ValueError("Usuario no válido")
        except Exception as e:
            raise ValueError(f"Error al verificar credenciales: {e}")
    
    def login_cliente(self, dui, pin):
        """
        Verificar credenciales de un cliente
        """
        try:
            usuario = self.repo.obtener_usuario_por_dui(dui)
            if usuario.rol == 'Cliente':
                if usuario.validar_pin(pin):
                    return usuario
                else:
                    raise ValueError("PIN no válido")
            else:
                raise ValueError("Usuario no válido")
        except Exception as e:
            raise ValueError(f"Error al verificar credenciales: {e}")
    
    def registrar_cliente(self, nombres, apellidos, dui, pin):
        """
        Registrar un nuevo cliente
        """
        try:
            nuevo_id = self.repo.obtenerSiguienteId()
            
            nuevo_cliente = Cliente(nuevo_id, nombres, apellidos, dui, pin, 'Cliente')
            self.repo.guardar_usuario(nuevo_cliente)
            
            return nuevo_cliente
        except Exception as e:
            raise ValueError(f"Error al registrar cliente: {e}")
        
    def registrar_admin(self, nombres, apellidos, rol, userName=None):
        """
        Registrar un nuevo administrador
        """
        try:
            nuevo_id = self.repo.obtenerSiguienteId()
            
            nuevo_admin = Administrador(nuevo_id, nombres, apellidos, rol, userName)
            self.repo.guardar_usuario(nuevo_admin)
            
            return nuevo_admin
        except Exception as e:
            raise ValueError(f"Error al registrar administrador: {e}")
    
    def cambiar_pin(self, dui, nuevo_pin):
        """
        Cambiar el PIN de un cliente
        """
        try:
            usuario = self.repo.obtener_usuario(dui)
            if usuario.rol == 'Cliente':
                if nuevo_pin != usuario.pin and len(nuevo_pin) == 4 and nuevo_pin.isdigit():
                    usuario.pin = nuevo_pin
                    self.repo.guardar_usuario(usuario)
                    return usuario
                else:
                    raise ValueError("El PIN debe ser un número de 4 dígitos")
        except Exception as e:
            raise ValueError(f"Error al cambiar PIN: {e}")