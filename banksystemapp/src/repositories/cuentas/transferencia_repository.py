import csv
import os
from ...models.cuentas.transferencia import Transferencia

class TransferenciaRepository:
    def __init__(self):
        # Definición de la ruta y columnas según el requerimiento [cite: 119, 121]
        self.archivo_csv = os.path.join("banksystemapp", "data", "transferencias.csv")
        self.headers = ["id_transferencia", "id_cuenta_origen", "id_cuenta_destino", "monto", "fecha_hora"]
        self._verificar_archivo()

    def _verificar_archivo(self):
        """Crea el archivo con encabezados si no existe[cite: 125]."""
        if not os.path.exists(self.archivo_csv):
            os.makedirs(os.path.dirname(self.archivo_csv), exist_ok=True)
            with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def obtener_todas(self):
        """
        Carga todas las transferencias. 
        Esencial para construir el grafo dirigido en NetworkX[cite: 103, 104].
        """
        transferencias = []
        try:
            with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    transferencias.append(Transferencia(
                        fila['id_transferencia'],
                        fila['id_cuenta_origen'],
                        fila['id_cuenta_destino'],
                        fila['monto'],
                        fila['fecha_hora']
                    ))
        except Exception as e:
            print(f"Error al leer transferencias: {e}")
        return transferencias

    def agregar(self, t: Transferencia):
        """
        Persiste una nueva transferencia entre cuentas[cite: 124].
        """
        try:
            with open(self.archivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writerow({
                    "id_transferencia": t.id_transferencia,
                    "id_cuenta_origen": t.id_origen,
                    "id_cuenta_destino": t.id_destino,
                    "monto": t.monto,
                    "fecha_hora": t.fecha_hora
                })
        except Exception as e:
            print(f"Error al registrar transferencia: {e}")