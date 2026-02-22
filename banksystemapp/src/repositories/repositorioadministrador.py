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
            campos = ['userId', 'nombres', 'apellidos', 'dui', 'password', 'rol', 'userName']
            writer = csv.DictWriter(archivo, fieldnames=campos)
            if not archivo_existe:
                writer.writeheader()
            writer.writerow({
                'userId': admin.userId,
                'nombres': admin.nombres,
                'apellidos': admin.apellidos,
                'dui': admin.dui,
                'password': admin.password,
                'rol': admin.rol,
                'userName': admin.userName
            })

    def buscarPorUserName(self, userName):
        if not os.path.exists(self.archivo):
            return None
        with open(self.archivo, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for linea in reader:
                if linea['userName'] == userName and linea['rol'] == 'administrador':
                    return Administrador(
                        int(linea['userId']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['password'],
                        linea['rol'],
                        linea['userName']
                    )
        return None