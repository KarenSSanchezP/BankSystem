import csv
import os
from .repositorioUsuario import usuarioRepository
from ..models.usuarios.cliente import Cliente

class repositorioCliente(usuarioRepository):
    def __init__(self):
        super().__init__()

    def guardarCliente(self,cliente):
        archivoExiste=os.path.exists(self.archivo)
        with open(self.archivo,'a',encoding='utf-8',newline='') as archivo:
            campos=['id_usuario','nombres','apellidos','dui','pin','username','rol']
            writer=csv.DictWriter(archivo,fieldnames=campos)
            if not archivoExiste:
                writer.writeheader()
            writer.writerow({
                'id_usuario': cliente.userId,
                'nombres': cliente.nombres,
                'apellidos': cliente.apellidos,
                'dui': cliente.dui,
                'pin': cliente.password,
                'rol': cliente.rol,
                'username': cliente.userName
            })

    def buscarPorDui(self,dui):
        if not os.path.exists(self.archivo):
            return None
        with open(self.archivo, 'r', encoding='utf-8') as archivo:
            reader=csv.DictReader(archivo)
            for linea in reader:
                if linea['dui']==dui and linea['rol'].lower()=='cliente':
                    return Cliente(
                        int(linea['id_usuario']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['pin'],
                        linea['rol'],
                        linea['username']
                    )
        return None

    def listarTodos(self):
        clientes=[]
        if not os.path.exists(self.archivo):
            return clientes
        with open(self.archivo,'r',encoding='utf-8') as archivo:
            reader=csv.DictReader(archivo)
            for linea in reader:
                if linea['rol'].lower()=='cliente':
                    clientes.append(Cliente(
                        int(linea['id_usuario']),
                        linea['nombres'],
                        linea['apellidos'],
                        linea['dui'],
                        linea['pin'],
                        linea['rol'],
                        linea['username']
                    ))
        return clientes
