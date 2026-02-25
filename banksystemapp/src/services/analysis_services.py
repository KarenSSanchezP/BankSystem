import numpy as np
import pandas as pd
import os

class AnalisisService:
    def __init__(self):
        self.ruta_tx = os.path.join("banksystemapp", "data", "transacciones.csv")
        self.ruta_tr = os.path.join("banksystemapp", "data", "transferencias.csv")

    def cargar_datos(self):
        """Carga las transacciones y convierte la fecha a objeto datetime."""
        if not os.path.exists(self.ruta_tx): 
            return None
        df = pd.read_csv(self.ruta_tx)
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        return df

    # --- ANOMALÍA 1: Z-SCORE ---
    def detectar_zscore(self, id_cuenta):
        """Detecta montos atípicos usando z = (x - mu) / sigma"""
        df = self.cargar_datos()
        if df is None or df.empty: return []

        # Filtrar por cuenta y solo depósitos o gastos según definas
        datos_cuenta = df[df['id_cuenta'] == id_cuenta].copy()
        
        if datos_cuenta.empty: return []

        montos = datos_cuenta['monto'].to_numpy()
        media = np.mean(montos)
        desviacion = np.std(montos)
        
        if desviacion == 0: return []

        # Cálculo vectorizado (Sin ciclos for)
        z_scores = (montos - media) / desviacion
        
        # Filtramos donde |z| > 3
        anomalias = datos_cuenta[np.abs(z_scores) > 3]
        return anomalias

    # --- ANOMALÍA 2: STRUCTURING ---
    def detectar_structuring(self):
        """Detecta >= 4 depósitos <= $50 en un mismo día"""
        df = self.cargar_datos()
        if df is None or df.empty: return []

        # Solo depósitos
        depositos = df[df['tipo'] == 'DEPOSITO'].copy()
        depositos['fecha'] = depositos['fecha_hora'].dt.date
        
        # Agrupamos por cuenta y fecha, contando cuántos cumplen monto <= 50
        check_monto = depositos[depositos['monto'] <= 50]
        conteo = check_monto.groupby(['id_cuenta', 'fecha']).size()
        
        # Anomalía si el conteo es >= 4
        anomalias = conteo[conteo >= 4]
        return anomalias

    # --- ANOMALÍA 3: ACTIVIDAD NOCTURNA ---
    def detectar_actividad_nocturna(self, id_cuenta):
        """Detecta transacciones entre 21:00 y 04:00"""
        df = self.cargar_datos()
        if df is None or df.empty: return []

        datos_cuenta = df[df['id_cuenta'] == id_cuenta].copy()
        if datos_cuenta.empty: return []
        
        # Extraer la hora
        horas = datos_cuenta['fecha_hora'].dt.hour
        
        # Condición: >= 21 o < 4
        nocturnas = datos_cuenta[(horas >= 21) | (horas < 4)]
        
        # Comparación relativa simple (puedes compararlo con el promedio diario nocturno)
        return nocturnas
