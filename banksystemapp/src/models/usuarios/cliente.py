from .usuario import Usuario

class Cliente(Usuario):
    def __init__(self, userId, nombres, apellidos, dui, password, rol='cliente', userName=None):
        super().__init__(userId, nombres, apellidos, dui, password, rol, userName)

    def __str__(self):
        return f"[Cliente] {self._nombres} {self._apellidos} (User: {self._userName})"

# from.usuario import Usuario
# class  Cliente(Usuario):
#     def __init__(self, userId, nombres, apellidos, dui,pin, rol):
#         super().__init__(userId, nombres, apellidos, dui, pin, rol)

#     def __str__(self):
#         return f"[Cliente]{self._nombres}{self._apellidos}(User:{self._userName})"