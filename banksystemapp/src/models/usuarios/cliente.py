from .usuario import Usuario

class  Cliente(Usuario):
    def __init__(self, userId, nombres, apellidos, dui, pin, rol):
        self.validar_pin(pin)
        super().__init__(userId, nombres, apellidos, dui, pin, rol)
    
    def validar_pin(self, pin):
        if not (isinstance(pin, str) and len(pin) == 4 and pin.isdigit()):
            raise ValueError("El PIN debe ser un número de 4 dígitos")
        return True
    
    def __str__(self):
        return f"[Cliente] {self._nombres} {self._apellidos} (User: {self._userName})"