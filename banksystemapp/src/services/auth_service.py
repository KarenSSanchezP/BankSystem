from ..repositories.usuarios.repositorioUsuario import UsuarioRepository
from ..repositories.usuarios.repositorioAdministrador import RepositorioAdministrador
from ..repositories.usuarios.repositorioCliente import RepositorioCliente
from banksystemapp.src.models.usuarios.cliente import Cliente
from banksystemapp.src.models.usuarios.admin import Administrador

class AuthService:
    def __init__(self):
        self.repo_u = UsuarioRepository()
        self.repo_a = RepositorioAdministrador()
        self.repo_c = RepositorioCliente()
    
    def login_admin(self, username):
        """
        Verificar credenciales de un administrador
        """
        try:
            admin = self.repo_a.buscarPorUserName(username)
            if admin and admin.rol == 'Admin':
                return admin
            else:
                raise ValueError("Usuario no válido o no es administrador")
        except Exception as e:
            raise ValueError(f"Error al verificar credenciales: {e}")
    
    def login_cliente(self, dui, pin):
        """
        Verificar credenciales de un cliente
        """
        try:
            cliente = self.repo_c.buscarPorDui(dui)
            if cliente and cliente.pin == pin:
                return cliente
            else:
                raise ValueError("Usuario no válido o PIN incorrecto")
        except Exception as e:
            raise ValueError(f"Error al verificar credenciales: {e}")
    
    def registrar_cliente(self, nombres, apellidos, dui, pin):
        """
        Registrar un nuevo cliente
        """
        try:
            nuevo_id = self.repo.obtenerSiguienteId()
            
            nuevo_cliente = Cliente(nuevo_id, nombres, apellidos, dui, pin, 'Cliente')
            self.repo_c.guardar(nuevo_cliente)
            
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
            self.repo_a.guardar(nuevo_admin)
            
            return nuevo_admin
        except Exception as e:
            raise ValueError(f"Error al registrar administrador: {e}")
    
    def cambiar_pin(self, dui, nuevo_pin):
        """
        Cambiar el PIN de un cliente
        """
        try:
            cliente = self.repo_c.buscarPorDui(dui)
            if cliente.rol == 'Cliente':
                if nuevo_pin != cliente.pin and len(nuevo_pin) == 4 and nuevo_pin.isdigit():
                    cliente.pin = nuevo_pin
                    self.repo_c.guardar(cliente)
                    return cliente
                else:
                    raise ValueError("El PIN debe ser un número de 4 dígitos")
        except Exception as e:
            raise ValueError(f"Error al cambiar PIN: {e}")