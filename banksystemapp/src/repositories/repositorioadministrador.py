import csv
import os
from .repositorioUsuario import usuarioRepository
from ..models.usuarios.admin import Administrador

class RepositorioAdministrador(usuarioRepository):
    def __init__(self):
        super().__init__()

    def guardar(self, admin: Administrador):
        archivo_existe = os.path.exists(self.archivo)
        with open(self.archivo, 'a', encoding='utf-8', newline='') as archivo:
            campos = ['id_usuario', 'nombres', 'apellidos', 'dui', 'pin', 'username', 'rol']
            writer = csv.DictWriter(archivo, fieldnames=campos)
            if not archivo_existe:
                writer.writeheader()
            writer.writerow({
                'id_usuario': admin.userId,
                'nombres': admin.nombres,
                'apellidos': admin.apellidos,
                'dui': admin.dui,
                'pin': admin.password,
                'rol': admin.rol,
                'username': admin.userName
            })

    def buscarPorUserName(self, userName):
        if not os.path.exists(self.archivo):
            return None
        with open(self.archivo, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for linea in reader:
                if linea['rol'].lower() == 'admin':
                    admin = Administrador(
                        int(linea['id_usuario']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['pin'],
                        linea['rol'],
                        linea['username'] if linea['username'] else None
                    )
                    if admin.userName == userName:
                        return admin
        return None
