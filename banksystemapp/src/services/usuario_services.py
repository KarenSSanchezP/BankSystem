from ..repositories.repositorioCliente import RepositorioCliente
from ..repositories.repositorioAdministrador import RepositorioAdministrador
from ..models.usuarios.cliente import Cliente
from ..models.usuarios.admin import Administrador

class UsuarioService:
    def __init__(self):
        self._repo_cliente = RepositorioCliente()
        self._repo_admin = RepositorioAdministrador()

    def crear_cliente(self, nombres, apellidos, dui, password):
        if self._repo_cliente.buscarPorDui(dui):
            return False, "Ya existe un cliente con ese DUI."
        nuevo_id = self._repo_cliente.obtenerSiguienteId()
        cliente = Cliente(nuevo_id, nombres, apellidos, dui, password)
        self._repo_cliente.guardar(cliente)
        return True, f"Cliente creado. Username: {cliente.userName}"

    def obtener_cliente(self, dui):
        cliente = self._repo_cliente.buscarPorDui(dui)
        if not cliente:
            return False, "Cliente no encontrado."
        return True, cliente

    def actualizar_cliente(self, dui, nuevos_datos: dict):
        # nuevos_datos = {'nombres': ..., 'apellidos': ..., 'password': ...}
        clientes = self._repo_cliente.listarTodos()
        todos = self._repo_admin.listarTodos() if hasattr(self._repo_admin, 'listarTodos') else []
        encontrado = False
        for c in clientes:
            if c.dui == dui:
                encontrado = True
                break
        if not encontrado:
            return False, "Cliente no encontrado."
        self._repo_cliente.actualizar(dui, nuevos_datos)
        return True, "Cliente actualizado."

    def eliminar_cliente(self, dui):
        if not self._repo_cliente.buscarPorDui(dui):
            return False, "Cliente no encontrado."
        self._repo_cliente.eliminar(dui)
        return True, "Cliente eliminado."

    def listar_clientes(self):
        return self._repo_cliente.listarTodos()


    def crear_admin(self, nombres, apellidos, dui, password):
        nuevo_id = self._repo_admin.obtenerSiguienteId()
        admin = Administrador(nuevo_id, nombres, apellidos, dui, password)
        self._repo_admin.guardar(admin)
        return True, f"Admin creado. Username: {admin.userName}"

    def obtener_admin(self, userName):
        admin = self._repo_admin.buscarPorUserName(userName)
        if not admin:
            return False, "Administrador no encontrado."
        return True, admin

    def listar_admins(self):
        return self._repo_admin.listarTodos()


    def cambiar_password(self, dui, password_actual, password_nueva, rol='cliente'):
        if rol == 'cliente':
            usuario = self._repo_cliente.buscarPorDui(dui)
        else:
            usuario = self._repo_admin.buscarPorUserName(dui)

        if not usuario:
            return False, "Usuario no encontrado."
        if not usuario.verificarPassword(password_actual):
            return False, "Contraseña actual incorrecta."
        if rol == 'cliente':
            self._repo_cliente.actualizar(dui, {'password': password_nueva})
        else:
            self._repo_admin.actualizar(dui, {'password': password_nueva})
        return True, "Contraseña actualizada."