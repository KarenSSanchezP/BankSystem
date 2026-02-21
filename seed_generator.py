import os, csv

def leer_ids_existentes(ruta, columna_id_index=0):
    """Lee los IDs existentes de un archivo CSV"""
    ids_existentes = set()
    if os.path.exists(ruta):
        try:
            with open(ruta, mode='r', newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                siguiente(lector)  # Saltar encabezados
                for fila in lector:
                    if fila:  # Si la fila no está vacía
                        ids_existentes.add(fila[columna_id_index])
        except Exception as e:
            print(f"Error al leer {ruta}: {e}")
    return ids_existentes

def siguiente(iterador):
    """Intenta obtener el siguiente elemento de un iterador"""
    try:
        return next(iterador)
    except StopIteration:
        return None

def filtrar_duplicados(datos, ids_existentes, columna_id_index=0):
    """Filtra registros duplicados basándose en los IDs existentes"""
    encabezados = datos[0]
    registros_filtrados = [encabezados]
    
    for registro in datos[1:]:
        if registro[columna_id_index] not in ids_existentes:
            registros_filtrados.append(registro)
    
    return registros_filtrados

def generar_archivos_seed():
    # Asegurarnos de que la carpeta data/ exista en banksystemapp/
    os.makedirs('banksystemapp/data', exist_ok=True)

    # 1. Datos de Usuarios
    usuarios = [
        ['id_usuario', 'nombres', 'apellidos', 'dui', 'pin', 'username', 'rol'],
        ['1', 'Juan', 'Perez', '', '', 'JP1', 'Admin'],
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

    # Definir archivos con índice de columna ID
    archivos = {
        'banksystemapp/data/usuarios.csv': (usuarios, 0),
        'banksystemapp/data/cuentas.csv': (cuentas, 0),
        'banksystemapp/data/transacciones.csv': (transacciones, 0),
        'banksystemapp/data/transferencias.csv': (transferencias, 0)
    }

    for ruta, (datos, columna_id) in archivos.items():
        # Leer IDs existentes
        ids_existentes = leer_ids_existentes(ruta, columna_id)
        
        # Filtrar duplicados
        datos_filtrados = filtrar_duplicados(datos, ids_existentes, columna_id)
        
        # Si hay datos nuevos (además de encabezados)
        if len(datos_filtrados) > 1:
            # Si el archivo existe, leer datos anteriores
            datos_anteriores = []
            if os.path.exists(ruta):
                with open(ruta, mode='r', newline='', encoding='utf-8') as archivo:
                    lector = csv.reader(archivo)
                    datos_anteriores = list(lector)
            
            # Combinar datos anteriores + nuevos datos (sin encabezados repetidos)
            datos_combinados = datos_anteriores if datos_anteriores else [datos_filtrados[0]]
            datos_combinados.extend(datos_filtrados[1:])
            
            # Escribir datos combinados
            with open(ruta, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerows(datos_combinados)
            print(f"✓ {ruta} - {len(datos_filtrados) - 1} nuevo(s) registro(s) añadido(s)")
        else:
            if os.path.exists(ruta):
                print(f"✓ {ruta} - Sin registros nuevos (no hay duplicados)")
            else:
                # Si el archivo no existe y solo hay encabezados, crearlo
                with open(ruta, mode='w', newline='', encoding='utf-8') as archivo:
                    escritor = csv.writer(archivo)
                    escritor.writerows(datos_filtrados)
                print(f"✓ {ruta} - Archivo creado")

if __name__ == '__main__':
    generar_archivos_seed()
    print("\n¡Seed de datos generado exitosamente!")