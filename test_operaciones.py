from banksystemapp.src.services.cuenta_service import CuentaService
from banksystemapp.src.repositories.cuenta_repository import CuentaRepository

def test_sistema_financiero():
    service = CuentaService()
    repo = CuentaRepository()

    print("="*40)
    print(" INICIANDO TEST CON DATOS PROPORCIONADOS ")
    print("="*40)

    # 1. Test de Retiro Exitoso (C001 tiene $8000.0)
    print("\n[TEST 1] Retiro de C001:")
    exito1, msg1 = service.retirar("C001", 1500.0)
    print(f"Estado: {'✓' if exito1 else 'X'} | {msg1}")

    # 2. Test de Saldo Insuficiente (C005 tiene $300.0)
    print("\n[TEST 2] Retiro excesivo de C005 (Saldo: $300):")
    exito2, msg2 = service.retirar("C005", 500.0)
    print(f"Estado: {'✓' if not exito2 else 'X'} | {msg2}")

    # 3. Test de Transferencia (De C002: $2300 a C006: $450)
    print("\n[TEST 3] Transferencia C002 -> C006 por $300:")
    exito3, msg3 = service.transferir("C002", "C006", 300.0)
    print(f"Estado: {'✓' if exito3 else 'X'} | {msg3}")

    # 4. Test de Validación de Monto Negativo
    print("\n[TEST 4] Intento de depósito negativo en C003:")
    exito4, msg4 = service.depositar("C003", 100.0)
    print(f"Estado: {'✓' if not exito4 else 'X'} | {msg4}")

    # 5. Verificación de Persistencia en el CSV
    print("\n" + "="*40)
    print(" RESUMEN DE SALDOS FINALES (POST-TEST) ")
    print("="*40)
    cuentas_finales = repo.obtener_todas()
    interes = ["C001", "C002", "C005", "C006"]
    
    for c in cuentas_finales:
        if c.id_cuenta in interes:
            print(f"Cuenta: {c.id_cuenta} | Saldo Final: ${c.saldo:,.2f} | Estado: {c.estado}")

if __name__ == "__main__":
    test_sistema_financiero()