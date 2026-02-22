from abc import ABC, abstractmethod

class Usuario(ABC):
  def __init__(self,userId,nombres,apellidos,dui,password,rol,userName=None):
        self._userId=userId
        self._nombres=nombres
        self._apellidos=apellidos
        self._dui=dui
        self._password=password
        self._rol=rol
        self._userName=userName
    
        if userName:
            self._userName=userName
        else:
            self._userName=self.crearUserName()

        @property
        def userId(self):
            return self._userId
        
        @property
        def nombres(self):
            return self.nombres
      
        @property
        def apellidos(self):
            return self._apellidos
    
        @property
        def dui(self):
            return self._dui
        

        @property
        def password(self):
            return self._password
    
        @property
        def rol(self):
            return self._rol
    
        @abstractmethod
        def crearUserName(self):
            inicialNombre=self.nombres[0]
            inicialApellido=self.apellidos[0]
            return f"{inicialNombre}{inicialApellido}{self.userId}"
    
        @property
        def userName(self):
            return self._userName
            