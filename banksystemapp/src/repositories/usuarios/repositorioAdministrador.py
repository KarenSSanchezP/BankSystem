import csv
import os
from .repositorioUsuario import UsuarioRepository
from banksystemapp.src.models.usuarios.admin import Administrador

class RepositorioAdministrador(UsuarioRepository):
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
                if linea['userName'] == userName and linea['rol'] == 'Admin':
                    return Administrador(
                        linea['userId'],
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['password'],
                        linea['rol'],
                        linea['userName']
                    )
        return None
        
    def actualizar(self, userName, nuevos_datos: dict):
        """Actualiza los datos de un administrador por su userName."""
        with open(self.archivo, 'r', encoding='utf-8') as f:
            filas = list(csv.DictReader(f))
        
        with open(self.archivo, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self._campos())
            writer.writeheader()
            for fila in filas:
                if fila['userName'] == userName and fila['rol'] == 'Admin':
                    fila['nombres'] = nuevos_datos.get('nombres', fila['nombres'])
                    fila['apellidos'] = nuevos_datos.get('apellidos', fila['apellidos'])
                    fila['password'] = nuevos_datos.get('password', fila['password'])
                writer.writerow(fila)

    def eliminar(self, userName):
        """Elimina un administrador del CSV por su userName."""
        with open(self.archivo, 'r', encoding='utf-8') as f:
            filas = list(csv.DictReader(f))

        with open(self.archivo, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self._campos())
            writer.writeheader()
            for fila in filas:
                if not (fila['userName'] == userName and fila['rol'] == 'Admin'):
                    writer.writerow(fila)

    def listarTodos(self):
        """Retorna todos los administradores registrados."""
        admins = []
        if not os.path.exists(self.archivo):
            return admins
        with open(self.archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for linea in reader:
                if linea['rol'] == 'Admin':
                    admins.append(Administrador(
                        linea['userId'],
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['password'],
                        linea['rol'],
                        linea['userName']
                    ))
        return admins