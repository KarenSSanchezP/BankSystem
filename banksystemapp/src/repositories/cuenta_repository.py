import csv
import os
from ..models.cuentas.cuenta_bancaria import CuentaBancaria

class CuentaRepository:
    """
    Principio SOLID: Single Responsibility — solo persiste y recupera CuentasBancarias.
    """
    def __init__(self):
        self.archivo = os.path.join('banksystemapp', 'data', 'cuentas.csv')
        self._campos = ['id_cuenta', 'dui_propietario', 'tipo', 'saldo', 'estado']
        self._verificar_archivo()

    def _verificar_archivo(self):
        if not os.path.exists(self.archivo):
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            with open(self.archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self._campos)
                writer.writeheader()

    def obtener_todas(self) -> list:
        """Carga todas las cuentas al iniciar el programa."""
        cuentas = []
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
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

    def buscar_por_id(self, id_cuenta) -> CuentaBancaria:
        """Busca una cuenta por su ID."""
        for cuenta in self.obtener_todas():
            if cuenta.id_cuenta == id_cuenta:
                return cuenta
        return None

    def buscar_por_dui(self, dui) -> list:
        """Retorna todas las cuentas de un cliente por su DUI."""
        return [c for c in self.obtener_todas() if c.dui_propietario == dui]

    def guardar_todas(self, lista_cuentas: list):
        """Persiste todos los cambios en el archivo."""
        try:
            with open(self.archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self._campos)
                writer.writeheader()
                for c in lista_cuentas:
                    writer.writerow({
                        'id_cuenta': c.id_cuenta,
                        'dui_propietario': c.dui_propietario,
                        'tipo': c.tipo,
                        'saldo': c.saldo,
                        'estado': c.estado
                    })
        except Exception as e:
            print(f"Error al guardar cuentas: {e}")

    def agregar(self, cuenta: CuentaBancaria):
        """Agrega una cuenta nueva al CSV."""
        archivo_existe = os.path.exists(self.archivo)
        with open(self.archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._campos)
            if not archivo_existe:
                writer.writeheader()
            writer.writerow({
                'id_cuenta': cuenta.id_cuenta,
                'dui_propietario': cuenta.dui_propietario,
                'tipo': cuenta.tipo,
                'saldo': cuenta.saldo,
                'estado': cuenta.estado
            })

    def obtenerSiguienteId(self) -> str:
        """Genera el siguiente ID de cuenta (ej: C010)."""
        cuentas = self.obtener_todas()
        if not cuentas:
            return 'C001'
        numeros = []
        for c in cuentas:
            try:
                numeros.append(int(c.id_cuenta[1:]))
            except ValueError:
                pass
        siguiente = max(numeros) + 1 if numeros else 1
        return f"C{siguiente:03d}"
    
    def actualizar(self, id_cuenta, nuevos_datos: dict):
        """Actualiza los datos de una cuenta por su ID."""
        cuentas = self.obtener_todas()

        with open(self.archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._campos)
            writer.writeheader()
            for c in cuentas:
                if c.id_cuenta == id_cuenta:
                    writer.writerow({
                        'id_cuenta': c.id_cuenta,
                        'dui_propietario': c.dui_propietario,
                        'tipo': nuevos_datos.get('tipo', c.tipo),
                        'saldo': nuevos_datos.get('saldo', c.saldo),
                        'estado': nuevos_datos.get('estado', c.estado)
                    })
                else:
                    writer.writerow({
                        'id_cuenta': c.id_cuenta,
                        'dui_propietario': c.dui_propietario,
                        'tipo': c.tipo,
                        'saldo': c.saldo,
                        'estado': c.estado
                    })

    def eliminar(self, id_cuenta):
        """Elimina una cuenta del CSV por su ID."""
        cuentas = self.obtener_todas()
        restantes = [c for c in cuentas if c.id_cuenta != id_cuenta]

        with open(self.archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._campos)
            writer.writeheader()
            for c in restantes:
                writer.writerow({
                    'id_cuenta': c.id_cuenta,
                    'dui_propietario': c.dui_propietario,
                    'tipo': c.tipo,
                    'saldo': c.saldo,
                    'estado': c.estado
                })
        
# import csv
# import os
# from ..models.cuentas.cuenta_Bancaria import CuentaBancaria

# class CuentaRepository:
#     def __init__(self):
#         # Ruta dinámica hacia la carpeta data
#         self.archivo_csv = os.path.join("banksystemapp", "data", "cuentas.csv")
#         self.headers = ["id_cuenta", "dui_propietario", "tipo", "saldo", "estado"]
#         self._verificar_archivo()

#     def _verificar_archivo(self):
#         """Crea el archivo con encabezados (en caso si no existieran)"""
#         if not os.path.exists(self.archivo_csv):
#             os.makedirs(os.path.dirname(self.archivo_csv), exist_ok=True)
#             with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as f:
#                 writer = csv.DictWriter(f, fieldnames=self.headers)
#                 writer.writeheader()

#     def obtener_todas(self):
#         """Carga los datos al iniciar el programa."""
#         cuentas = []
#         try:
#             with open(self.archivo_csv, mode='r', encoding='utf-8') as f:
#                 reader = csv.DictReader(f)
#                 for fila in reader:
#                     cuentas.append(CuentaBancaria(
#                         fila['id_cuenta'],
#                         fila['dui_propietario'],
#                         fila['tipo'],
#                         fila['saldo'],
#                         fila['estado']
#                     ))
#         except Exception as e:
#             print(f"Error al leer cuentas: {e}")
#         return cuentas

#     def guardar_todas(self, lista_cuentas):
#         """Persiste todos los cambios en el archivo."""
#         try:
#             with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as f:
#                 writer = csv.DictWriter(f, fieldnames=self.headers)
#                 writer.writeheader()
#                 for c in lista_cuentas:
#                     writer.writerow({
#                         "id_cuenta": c.id_cuenta,
#                         "dui_propietario": c.dui_propietario,
#                         "tipo": c.tipo,
#                         "saldo": c.saldo,
#                         "estado": c.estado
#                     })
#         except Exception as e:
#             print(f"Error al guardar cuentas: {e}") 