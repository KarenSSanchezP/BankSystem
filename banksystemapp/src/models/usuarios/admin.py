from .usuario import Usuario
class  Administrador(Usuario):
    def __init__(self, userId, nombres, apellidos, rol, userName=None):
        super().__init__(userId, nombres, apellidos, None, None, rol, userName)

    def __str__(self):
        return f"[Administrador] {self._nombres} {self._apellidos} (User: {self._userName})"