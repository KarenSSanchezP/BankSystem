from .usuario import Usuario

class Cliente(Usuario):
    def __init__(self, userId, nombres, apellidos, dui, pin, rol, userName=None):
        super().__init__(userId, nombres, apellidos, dui, pin, rol, userName)

    def crearUserName(self):
        inicialNombre = self.nombres[0] if self.nombres else "X"
        inicialApellido = self.apellidos[0] if self.apellidos else "X"
        return f"{inicialNombre}{inicialApellido}{self.userId}"

    def __str__(self):
        return f"[Cliente] {self._nombres} {self._apellidos} (User: {self._userName})"
