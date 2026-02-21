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
            if self.nombres == None:
                print("Lllenar los espacios")
            else:
                return self.nombres
      
        @property
        def apellidos(self):
            if self.apellidos == None:
                print("Llenar los espacios")
            else:
                return self._apellidos
    
        @property
        def dui(self):
            return self._dui
        
        @abstractmethod
        def verificarPassword(self,password):
            return self._password == password

        @property
        def password(self):
            return self._password
    
        @property
        def rol(self):
            return self._rol
    
        @abstractmethod
        def crearUserName(self):
            nombre1=self._nombre
            apellido1=self._apellido
            nombre=(nombre1+apellido1).split('')
            nombre1=[0]
            apellido1=[0]
            return f"{nombre1}{apellido1}{self.userId}"
    
        @property
        def userName(self):
            return self._userName
            