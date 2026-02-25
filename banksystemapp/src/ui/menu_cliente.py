from .menu_base import MenuBase
from ..services.cuenta_service import CuentaService
from ..repositories.cuenta_repository import CuentaRepository
from ..repositories.cuentas.transaccion_repository import TransaccionRepository
from ..repositories.cuentas.transferencia_repository import TransferenciaRepository

class MenuCliente(MenuBase):
    def __init__(self, usuario_logueado):
        super().__init__()
        self.usuario = usuario_logueado
        # Integración de servicios y repositorios para la lógica de negocio
        self.cuenta_service = CuentaService()
        self.cuenta_repo = CuentaRepository()
        self.transaccion_repo = TransaccionRepository()
        self.transferencia_repo = TransferenciaRepository()
        
        self.opciones = [
            '1. Saldo de sus cuentas',
            '2. Historial de movimientos',
            '3. Depositar',
            '4. Retirar',
            '5. Transferir entre cuentas',
            '6. Cerrar sesion'
        ]
    
    def ejecutar(self):
        while True:
            self.mostrar_encabezado(f"Panel de cliente - {self.usuario.userName}", 40)
            for opcion in self.opciones:
                print(f"\t{opcion}")
            
            try:
                seleccion = self.pedir_opcion(self.opciones)
                if seleccion == '1':
                    self.saldo_cuentas()
                elif seleccion == '2':
                    self.historial_movimientos()
                elif seleccion == '3':
                    self.depositar()
                elif seleccion == '4':
                    self.retirar()
                elif seleccion == '5':
                    self.transferir_entre_cuentas()
                elif seleccion == '6':
                    self.salir("Cerrando sesión del cliente...")
                    break
            except ValueError as e:
                print(f"Error: {e}")
                self.pausa(2)
                self.limpiar_consola()

    def _obtener_mis_cuentas(self):
        """Retorna la lista de cuentas que pertenecen al DUI del usuario logueado[cite: 25]."""
        return self.cuenta_repo.buscar_por_dui(self.usuario.dui)

    def _seleccionar_cuenta(self, mensaje="Seleccione una cuenta: "):
        """Utilidad para que el cliente elija una de sus cuentas."""
        mis_cuentas = self._obtener_mis_cuentas()
        if not mis_cuentas:
            print("No tienes cuentas registradas.")
            return None
        
        for i, cuenta in enumerate(mis_cuentas):
            print(f"{i+1}. {cuenta}")
        
        opc = input(mensaje)
        try:
            indice = int(opc) - 1
            if 0 <= indice < len(mis_cuentas):
                return mis_cuentas[indice]
        except ValueError:
            pass
        print("Selección inválida.")
        return None

    def saldo_cuentas(self):
        """Muestra el saldo de todas las cuentas del cliente."""
        self.mostrar_encabezado("Saldo de sus cuentas", 40, simbolo="-", es_salto_de_linea=True)
        mis_cuentas = self._obtener_mis_cuentas()
        if mis_cuentas:
            for c in mis_cuentas:
                print(f"-> {c}")
        else:
            print("No se encontraron cuentas asociadas a su DUI.")
        self.continuar()
        self.limpiar_consola()

    def historial_movimientos(self):
        """Muestra transacciones y transferencias relacionadas con el cliente."""
        self.mostrar_encabezado("Historial de movimientos", 40, simbolo="-", es_salto_de_linea=True)
        mis_cuentas = self._obtener_mis_cuentas()
        ids_mis_cuentas = [c.id_cuenta for c in mis_cuentas]
        
        print("\n--- Transacciones (Depósitos/Retiros) ---")
        todas_tx = self.transaccion_repo.obtener_todas()
        encontradas_tx = [t for t in todas_tx if t.id_cuenta in ids_mis_cuentas]
        for t in encontradas_tx:
            print(t)
            
        print("\n--- Transferencias ---")
        todas_tr = self.transferencia_repo.obtener_todas()
        encontradas_tr = [tr for tr in todas_tr if tr.id_origen in ids_mis_cuentas or tr.id_destino in ids_mis_cuentas]
        for tr in encontradas_tr:
            print(tr)
            
        self.continuar()
        self.limpiar_consola()

    def depositar(self):
        """Permite al cliente realizar un depósito en una de sus cuentas."""
        self.mostrar_encabezado("Depositar", 40, simbolo="-", es_salto_de_linea=True)
        cuenta = self._seleccionar_cuenta()
        if cuenta:
            try:
                monto = float(input("Ingrese el monto a depositar: $"))
                exito, msg = self.cuenta_service.depositar(cuenta.id_cuenta, monto)
                print(msg)
            except ValueError:
                print("Error: Ingrese un monto numérico válido.")
        self.continuar()
        self.limpiar_consola()

    def retirar(self):
        """Permite al cliente retirar dinero validando saldo y estado[cite: 35, 41]."""
        self.mostrar_encabezado("Retirar", 40, simbolo="-", es_salto_de_linea=True)
        cuenta = self._seleccionar_cuenta()
        if cuenta:
            try:
                monto = float(input("Ingrese el monto a retirar: $"))
                exito, msg = self.cuenta_service.retirar(cuenta.id_cuenta, monto)
                print(msg)
            except ValueError:
                print("Error: Ingrese un monto numérico válido.")
        self.continuar()
        self.limpiar_consola()

    def transferir_entre_cuentas(self):
        """Permite transferencias a cuentas propias o terceros[cite: 36, 42]."""
        self.mostrar_encabezado("Transferir entre cuentas", 40, simbolo="-", es_salto_de_linea=True)
        cuenta_origen = self._seleccionar_cuenta("Seleccione la cuenta de origen: ")
        if cuenta_origen:
            id_destino = input("Ingrese el ID de la cuenta destino (ej. C001): ").strip().upper()
            try:
                monto = float(input("Ingrese el monto a transferir: $"))
                exito, msg = self.cuenta_service.transferir(cuenta_origen.id_cuenta, id_destino, monto)
                print(msg)
            except ValueError:
                print("Error: Ingrese un monto numérico válido.")
        self.continuar()
        self.limpiar_consola()