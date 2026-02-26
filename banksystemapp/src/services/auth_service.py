from ..repositories.repositorioadministrador import RepositorioAdministrador
from ..repositories.repositorioCliente import repositorioCliente

class AuthService:
    def __init__(self):
        self.repo_admin = RepositorioAdministrador()
        self.repo_cliente = repositorioCliente()

    def login_admin(self, username):
        admin = self.repo_admin.buscarPorUserName(username)
        if hasattr(admin, 'password'): 
            if admin:
                return admin
        if admin:
            return admin
        raise Exception("Administrador no encontrado")

    def login_cliente(self, dui, pin):
        cliente = self.repo_cliente.buscarPorDui(dui)
        if cliente and cliente.password == pin:
            return cliente
        raise Exception("Credenciales de cliente incorrectas")
