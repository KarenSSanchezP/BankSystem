from banksystemapp.src.services.cuenta_services import CuentaService
from banksystemapp.src.repositories.cuenta_repository import CuentaRepository

def verificar_test():
    service = CuentaService()
    repo_cuentas = CuentaRepository()

    print("--- INICIANDO TEST DE OPERACIONES ---")

    # 1. Probar Depósito Exitoso (Usando la cuenta C002 del seed)
    print("\n[Test 1: Depósito]")
    exito, mensaje = service.depositar("C002", 500.0)
    print(f"Resultado: {mensaje}")

    # 2. Probar Transferencia Exitosa (De C004 a C001)
    # C004 tiene $5000.00 en el seed
    print("\n[Test 2: Transferencia]")
    exito, mensaje = service.transferir("C001", "C004", 1000.0)
    print(f"Resultado: {mensaje}")

    # 3. Probar Validación: Saldo Insuficiente (C005 solo tiene $300.00)
    print("\n[Test 3: Validación Saldo Insuficiente]")
    exito, mensaje = service.transferir("C005", "C001", 5000.0)
    print(f"Resultado: {mensaje if not exito else 'Error: Debería haber fallado'}")

    # 4. Probar Validación: Monto Negativo
    print("\n[Test 4: Validación Monto > 0]")
    exito, mensaje = service.depositar("C001", -50.0)
    print(f"Resultado: {mensaje if not exito else 'Error: Debería haber fallado'}")

    # 5. Verificar Persistencia Final
    print("\n--- VERIFICACIÓN DE PERSISTENCIA ---")
    todas = repo_cuentas.obtener_todas()
    for c in todas:
        if c.id_cuenta in ["C001", "C004"]:
            print(f"Estado Final {c.id_cuenta}: Saldo ${c.saldo}")

if __name__ == "__main__":
    verificar_test()