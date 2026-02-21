import csv
import os
from ..models.cuentas.transaccion import Transaccion

class TransaccionRepository:
    def __init__(self):
        # Definición de la ruta y columnas según el requerimiento 
        self.archivo_csv = os.path.join("banksystemapp", "data", "transacciones.csv")
        self.headers = ["id_transaccion", "id_cuenta", "tipo", "monto", "fecha_hora"]
        self._verificar_archivo()

    def _verificar_archivo(self):
        """Crea el archivo con encabezados si no existe para asegurar la carga inicial."""
        if not os.path.exists(self.archivo_csv):
            os.makedirs(os.path.dirname(self.archivo_csv), exist_ok=True)
            with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def obtener_todas(self):
        """Lee todas las transacciones para el módulo de analítica."""
        transacciones = []
        try:
            with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    transacciones.append(Transaccion(
                        fila['id_transaccion'],
                        fila['id_cuenta'],
                        fila['tipo'],
                        fila['monto'],
                        fila['fecha_hora']
                    ))
        except Exception as e:
            print(f"Error al leer transacciones: {e}") 
        return transacciones

    def agregar(self, t: Transaccion):
        """Registra una nueva transacción al final del archivo."""
        try:
            with open(self.archivo_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writerow({ #escribimos la fila
                    "id_transaccion": t.id_transaccion,
                    "id_cuenta": t.id_cuenta,
                    "tipo": t.tipo,
                    "monto": t.monto,
                    "fecha_hora": t.fecha_hora
                })
        except Exception as e:
            print(f"Error al registrar transacción: {e}")