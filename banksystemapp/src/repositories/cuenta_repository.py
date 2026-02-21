import csv
import os
from ..models.cuentas.cuenta_Bancaria import CuentaBancaria

class CuentaRepository:
    def __init__(self):
        # Ruta dinámica hacia la carpeta data
        self.archivo_csv = os.path.join("banksystemapp", "data", "cuentas.csv")
        self.headers = ["id_cuenta", "dui_propietario", "tipo", "saldo", "estado"]
        self._verificar_archivo()

    def _verificar_archivo(self):
        """Crea el archivo con encabezados (en caso si no existieran)"""
        if not os.path.exists(self.archivo_csv):
            os.makedirs(os.path.dirname(self.archivo_csv), exist_ok=True)
            with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def obtener_todas(self):
        """Carga los datos al iniciar el programa."""
        cuentas = []
        try:
            with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    cuentas.append(CuentaBancaria(
                        fila['id_cuenta'],
                        fila['dui_propietario'],
                        fila['tipo'],
                        fila['saldo'],
                        fila['estado']
                    ))
        except Exception as e:
            print(f"Error al leer cuentas: {e}")
        return cuentas

    def guardar_todas(self, lista_cuentas):
        """Persiste todos los cambios en el archivo."""
        try:
            with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                for c in lista_cuentas:
                    writer.writerow({
                        "id_cuenta": c.id_cuenta,
                        "dui_propietario": c.dui_propietario,
                        "tipo": c.tipo,
                        "saldo": c.saldo,
                        "estado": c.estado
                    })
        except Exception as e:
            print(f"Error al guardar cuentas: {e}") 