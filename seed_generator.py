import os, csv

def generar_archivos_seed():
    # Asegurarnos de que la carpeta data/ exista
    os.makedirs('data', exist_ok=True)

    # 1. Datos de Usuarios
    usuarios = [
        ['id_usuario', 'nombres', 'apellidos', 'dui', 'pin', 'username', 'rol'],
        ['1', 'Juan', 'Perez', '', '', 'JP01', 'Admin'],
        ['2', 'Maria', 'Gonzalez', '01234567-1', '1111', '', 'Cliente'],
        ['3', 'Carlos', 'Hernandez', '02345678-2', '2222', '', 'Cliente'],
        ['4', 'Ana', 'Martinez', '03456789-3', '3333', '', 'Cliente'],
        ['5', 'Jose', 'Lopez', '04567890-4', '4444', '', 'Cliente'],
        ['6', 'Luis', 'Ramirez', '05678901-5', '5555', '', 'Cliente'],
        ['7', 'Carmen', 'Diaz', '06789012-6', '6666', '', 'Cliente'],
        ['8', 'Jorge', 'Cruz', '07890123-7', '7777', '', 'Cliente'],
        ['9', 'Rosa', 'Gomez', '08901234-8', '8888', '', 'Cliente'],
        ['10', 'Mario', 'Flores', '09012345-9', '9999', '', 'Cliente']
    ]

    # 2. Datos de Cuentas
    cuentas = [
        ['id_cuenta', 'dui_propietario', 'tipo', 'saldo', 'estado'],
        ['C001', '01234567-1', 'Ahorro', '2500.00', 'Activa'],
        ['C002', '02345678-2', 'Corriente', '800.00', 'Activa'],
        ['C003', '03456789-3', 'Ahorro', '1200.00', 'Activa'],
        ['C004', '04567890-4', 'Corriente', '5000.00', 'Activa'],
        ['C005', '05678901-5', 'Ahorro', '300.00', 'Activa'],
        ['C006', '06789012-6', 'Ahorro', '450.00', 'Activa'],
        ['C007', '07890123-7', 'Corriente', '1000.00', 'Activa'],
        ['C008', '08901234-8', 'Ahorro', '250.00', 'Activa'],
        ['C009', '09012345-9', 'Ahorro', '600.00', 'Activa']
    ]

    # 3. Datos de Transacciones (Incluye Z-Score en C001 y Structuring en C002)
    transacciones = [
        ['id_transaccion', 'id_cuenta', 'tipo', 'monto', 'fecha_hora'],
        ['T001', 'C001', 'DEPOSITO', '12.50', '2026-02-10 09:15:00'],
        ['T002', 'C001', 'DEPOSITO', '15.00', '2026-02-11 10:30:00'],
        ['T003', 'C001', 'DEPOSITO', '10.00', '2026-02-12 14:20:00'],
        ['T004', 'C001', 'DEPOSITO', '18.00', '2026-02-13 11:45:00'],
        ['T005', 'C001', 'DEPOSITO', '14.50', '2026-02-14 16:10:00'],
        ['T006', 'C001', 'DEPOSITO', '800.00', '2026-02-15 08:05:00'], # Anomalía Z-Score
        ['T007', 'C001', 'DEPOSITO', '11.00', '2026-02-16 09:20:00'],
        ['T008', 'C002', 'DEPOSITO', '45.00', '2026-02-16 08:10:00'], # Anomalía Structuring
        ['T009', 'C002', 'DEPOSITO', '45.00', '2026-02-16 10:15:00'],
        ['T010', 'C002', 'DEPOSITO', '45.00', '2026-02-16 12:30:00'],
        ['T011', 'C002', 'DEPOSITO', '45.00', '2026-02-16 14:45:00'],
        ['T012', 'C002', 'DEPOSITO', '45.00', '2026-02-16 16:50:00']
    ]

    # 4. Datos de Transferencias (Incluye Actividad Nocturna en C003 y Hub en C004)
    transferencias = [
        ['id_transferencia', 'id_cuenta_origen', 'id_cuenta_destino', 'monto', 'fecha_hora'],
        ['TR01', 'C003', 'C005', '25.00', '2026-02-17 23:15:00'], # Anomalía Nocturna
        ['TR02', 'C003', 'C006', '15.00', '2026-02-17 23:50:00'],
        ['TR03', 'C003', 'C007', '40.00', '2026-02-18 00:30:00'],
        ['TR04', 'C003', 'C008', '20.00', '2026-02-18 01:45:00'],
        ['TR05', 'C003', 'C009', '35.00', '2026-02-18 02:20:00'],
        ['TR06', 'C003', 'C001', '50.00', '2026-02-18 03:45:00'],
        ['TR07', 'C004', 'C005', '100.00', '2026-02-19 10:00:00'], # Grafo Hub (NetworkX)
        ['TR08', 'C004', 'C006', '150.00', '2026-02-19 11:00:00'],
        ['TR09', 'C004', 'C007', '200.00', '2026-02-19 12:00:00'],
        ['TR10', 'C004', 'C008', '120.00', '2026-02-19 13:00:00'],
        ['TR11', 'C004', 'C009', '180.00', '2026-02-19 14:00:00']
    ]

    # Escribir a CSV
    archivos = {
        'banksystemapp/data/usuarios.csv': usuarios,
        'banksystemapp/data/cuentas.csv': cuentas,
        'banksystemapp/data/transacciones.csv': transacciones,
        'banksystemapp/data/transferencias.csv': transferencias
    }

    for ruta, datos in archivos.items():
        with open(ruta, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(datos)
        print(f"Archivo generado: {ruta}")

if __name__ == '__main__':
    generar_archivos_seed()
    print("¡Seed de datos generado exitosamente!")