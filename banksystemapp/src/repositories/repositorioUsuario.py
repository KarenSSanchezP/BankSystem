import csv
import os
from abc import ABC, abstractmethod

class usuarioRepository(ABC):
    def __init__(self):
        self.archivo='banksystemapp/data/usuarios.csv'
        os.makedirs(os.path.dirname(self.archivo),exist_ok=True)


    def obtenerSiguienteId(self):
        if not os.path.exists(self.archivo):
            return 1 
        idMax=0
        try:
            with open(self.archivo, 'r', encoding='utf-8') as archivo:
                reader=csv.DictReader(archivo)
                for linea in reader:
                    idActual=int(linea['userId'])
                    if idActual > idMax:
                        idMax=idActual
        except Exception:
            return 1
        return idMax+1
        
