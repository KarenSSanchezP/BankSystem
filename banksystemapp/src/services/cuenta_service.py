from ..repositories.cuenta_repository import CuentaRepository
from ..repositories.cuentas.transaccion_repository import TransaccionRepository
from ..repositories.cuentas.transferencia_repository import TransferenciaRepository
from ..models.cuentas.transaccion import Transaccion
from ..models.cuentas.transferencia import Transferencia

class CuentaService:
    def __init__(self):
        self.cuenta_repo = CuentaRepository()
        self.transaccion_repo = TransaccionRepository()
        self.transferencia_repo = TransferenciaRepository()

    def depositar(self, id_cuenta, monto):
        """Lógica para realizar un depósito."""
        cuentas = self.cuenta_repo.obtener_todas()
        cuenta = next((c for c in cuentas if c.id_cuenta == id_cuenta), None)

        # Validaciones del PDF
        if not cuenta:
            return False, "La cuenta no existe."
        if cuenta.estado != "Activa": # [cite: 40]
            return False, "La cuenta está bloqueada."
        if monto <= 0: # 
            return False, "El monto debe ser mayor a 0."

        # Actualizar saldo y persistir
        cuenta.saldo += monto
        self.cuenta_repo.guardar_todas(cuentas)

        # Registrar transacción con ID autoincremental (puedes mejorar la lógica del ID)
        nueva_tx = Transaccion(f"T{len(self.transaccion_repo.obtener_todas()) + 1}", id_cuenta, "DEPOSITO", monto)
        self.transaccion_repo.agregar(nueva_tx) # [cite: 43]
        
        return True, f"Depósito exitoso. Nuevo saldo: ${cuenta.saldo}"

    def transferir(self, id_origen, id_destino, monto):
        """Lógica para transferencias entre cuentas propias o a terceros."""
        cuentas = self.cuenta_repo.obtener_todas()
        origen = next((c for c in cuentas if c.id_cuenta == id_origen), None)
        destino = next((c for c in cuentas if c.id_cuenta == id_destino), None)

        # Validaciones obligatorias
        if not origen or not destino:
            return False, "Una o ambas cuentas no existen."
        if origen.estado != "Activa" or destino.estado != "Activa": 
            return False, "Una de las cuentas está bloqueada."
        if monto <= 0: 
            return False, "El monto debe ser mayor a 0."
        if origen.saldo < monto: 
            return False, "Saldo insuficiente para transferir."

        # Ejecutar movimiento de dinero
        origen.saldo -= monto
        destino.saldo += monto
        self.cuenta_repo.guardar_todas(cuentas)

        # Registrar la transferencia para el módulo de grafos
        nueva_tr = Transferencia(f"TR{len(self.transferencia_repo.obtener_todas()) + 1}", id_origen, id_destino, monto)
        self.transferencia_repo.agregar(nueva_tr) # [cite: 43]

        return True, "Transferencia realizada con éxito."

    def retirar(self, id_cuenta, monto):
            """Lógica para realizar un retiro de efectivo."""
            cuentas = self.cuenta_repo.obtener_todas()
            cuenta = next((c for c in cuentas if c.id_cuenta == id_cuenta), None)

            # Validar que la cuenta existe cite: 40]
            if not cuenta:
                return False, "Error: La cuenta no existe."

            # Validar que la cuenta esté activa 
            if cuenta.estado != "Activa":
                return False, "Error: La cuenta está bloqueada."

            # Validar que el monto sea mayor a cero 
            if monto <= 0:
                return False, "Error: El monto a retirar debe ser mayor a 0."

            # Validar que tenga saldo suficiente 
            if cuenta.saldo < monto:
                return False, f"Error: Saldo insuficiente. Saldo actual: ${cuenta.saldo}"

            # Ejecutar retiro y actualizar persistencia 
            cuenta.saldo -= monto
            self.cuenta_repo.guardar_todas(cuentas)

            # Registrar en el historial de transacciones con fecha y hora 
            id_tx = f"T{len(self.transaccion_repo.obtener_todas()) + 1}"
            nueva_tx = Transaccion(id_tx, id_cuenta, "RETIRO", monto)
            self.transaccion_repo.agregar(nueva_tx)

            return True, f"Retiro exitoso. Nuevo saldo: ${cuenta.saldo}"