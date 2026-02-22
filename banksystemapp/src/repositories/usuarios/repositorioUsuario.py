import csv, os
from abc import ABC, abstractmethod
from banksystemapp.src.models.usuarios.usuario import Usuario

class UsuarioRepository(ABC):
    """
    Clase base abstracta para repositorios de usuarios.
    Principio SOLID: Single Responsibility — solo maneja acceso a datos de usuarios.
    Principio SOLID: Open/Closed — abierto para extender (Admin, Cliente), cerrado para modificar.
    """
    def __init__(self):
        self.archivo = os.path.join('banksystemapp', 'data', 'usuarios.csv')
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        self._verificar_archivo()

    def _verificar_archivo(self):
        """Crea el archivo con encabezados si no existe."""
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self._campos())
                writer.writeheader()

    def _campos(self):
        return ['userId', 'nombres', 'apellidos', 'dui', 'password', 'rol', 'userName']

    def obtenerSiguienteId(self):
        """Genera el siguiente ID autoincremental."""
        if not os.path.exists(self.archivo):
            return 1
        idMax = 0
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for linea in reader:
                    idActual = int(linea['userId'])
                    if idActual > idMax:
                        idMax = idActual
        except Exception:
            return 1
        return idMax + 1
    
    def obtener_usuario(self, userId):
        """
        Busca un usuario por su ID.
        """
        if not os.path.exists(self.archivo):
            return None
        with open(self.archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for linea in reader:
                if linea['userId'] == userId:
                    return Usuario(
                        int(linea['userId']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['password'],
                        linea['rol'],
                        linea['userName']
                    )
        return None

# import csv
# import os
# from abc import ABC, abstractmethod

# class usuarioRepository(ABC):
#     def __init__(self):
#         self.archivo='banksystemapp/data/usuarios.csv'
#         os.makedirs(os.path.dirname(self.archivo),exist_ok=True)


#     def obtenerSiguienteId(self):
#         if not os.path.exists(self.archivo):
#             return 1 
#         idMax=0
#         try:
#             with open(self.archivo, 'r', encoding='utf-8') as archivo:
#                 reader=csv.DictReader(archivo)
#                 for linea in reader:
#                     idActual=int(linea['userId'])
#                     if idActual > idMax:
#                         idMax=idActual
#         except Exception:
#             return 1
#         return idMax+1
        
