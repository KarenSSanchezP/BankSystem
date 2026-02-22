from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self,userId,nombres,apellidos,dui,pin,rol,userName=None):
        self._userId=userId
        self._nombres=nombres
        self._apellidos=apellidos
        self._dui=dui
        self._pin=pin
        self._rol=rol
        self._userName=userName if userName else self.crearUserName()

    @property
    def userId(self):
        return self._userId
    
    @property
    def nombres(self):
        return self._nombres

    @property
    def apellidos(self):
        return self._apellidos
    
    @property
    def dui(self):
        return self._dui
    
    @property
    def pin(self):
        return self._pin

    @property
    def rol(self):
        return self._rol

    def crearUserName(self):
        """ 
        Crea un nombre de usuario con las primeras letras de 
        cada nombre y apellido, seguido del ID de usuario 
        """
        inicialNombre = self._nombres[0].upper()
        inicialApellido = self._apellidos[0].upper()
        return f"{inicialNombre}{inicialApellido}{self.userId}"

    @property
    def userName(self):
        return self._userName
