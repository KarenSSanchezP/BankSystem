import csv
import os
from .repositorioUsuario import UsuarioRepository
from ..models.usuarios.cliente import Cliente

class RepositorioCliente(UsuarioRepository):
    """
    Principio SOLID: Single Responsibility — solo persiste y recupera Clientes.
    Principio SOLID: Liskov Substitution — extiende UsuarioRepository correctamente.
    """
    def __init__(self):
        super().__init__()

    def guardar(self, cliente: Cliente):
        """Agrega un cliente nuevo al CSV."""
        archivo_existe = os.path.exists(self.archivo)
        with open(self.archivo, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self._campos())
            if not archivo_existe:
                writer.writeheader()
            writer.writerow({
                'userId': cliente.userId,
                'nombres': cliente.nombres,
                'apellidos': cliente.apellidos,
                'dui': cliente.dui,
                'password': cliente.password,
                'rol': cliente.rol,
                'userName': cliente.userName
            })

    def buscarPorDui(self, dui) -> Cliente:
        """Busca un cliente por su DUI. Retorna None si no existe."""
        if not os.path.exists(self.archivo):
            return None
        with open(self.archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for linea in reader:
                if linea['dui'] == dui and linea['rol'] == 'cliente':
                    return Cliente(
                        int(linea['userId']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['password'],
                        linea['rol'],
                        linea['userName']
                    )
        return None

    def listarTodos(self) -> list:
        """Retorna todos los clientes registrados."""
        clientes = []
        if not os.path.exists(self.archivo):
            return clientes
        with open(self.archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for linea in reader:
                if linea['rol'] == 'cliente':
                    clientes.append(Cliente(
                        int(linea['userId']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['password'],
                        linea['rol'],
                        linea['userName']
                    ))
        return clientes
    
# import csv
# import os
# from .repositorioUsuario import usuarioRepository
# from ..models.usuarios.cliente import Cliente

# class repositorioCliente(usuarioRepository):
#     def __init__(self):
#         super().__init__()

#     def guardarCliente(self,cliente):
#         archivoExiste=os.path.exists(self.archivo)
#         with open(self.archivo,'a',encoding='utf-8',newline='') as archivo:
#             campos=['userId','nombre','apellido','dui','password','rol','userName']
#             writer=csv.DictWriter(archivo,fieldnames=campos)
#             if not archivoExiste:
#                 writer.writeheader()
#             writer.writerow({
#                 'userId': cliente.userId,
#                 'nombre': cliente.nombres,
#                 'apellido': cliente.apellidos,
#                 'dui': cliente.dui,
#                 'password': cliente.password,
#                 'rol': cliente.rol,
#                 'userName': cliente.userName
#             })

#     def buscarPorDui(self,dui):
#         if not os.path.exists(self.archivo):
#             return None
#         with open(self.archivo, 'r', encoding='utf-8') as archivo:
#             reader=csv.DictReader(archivo)
#             for linea in reader:
#                 if linea['dui']==dui and linea['rol']=='cliente':
#                     return Cliente(
#                         int(linea['userId']),
#                         linea['nombres'],
#                         linea['dui'],
#                         linea['password'],
#                         linea['rol'],
#                         linea['userName']
#                     )
#         return None

#     def listarTodos(self):
#         clientes=[]
#         if not os.path.exists(self.archivo):
#             return clientes
#         with open(self.archivo,'r',encoding='utf-8') as archivo:
#             reader=csv.DictReader(archivo)
#             for linea in reader:
#                 if linea['rol']=='cliente':
#                     clientes.append(Cliente(
#                         int(linea['userId']),
#                         linea['nombres'],
#                         linea['apellidos'],
#                         linea['dui'],
#                         linea['password'],
#                         linea['rol'],
#                         linea['userName']
#                     ))
#         return clientes
    