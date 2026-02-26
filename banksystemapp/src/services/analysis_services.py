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
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'], format='mixed', errors='coerce')
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

    # --- NUEVOS MÉTODOS REQUERIDOS POR LA UI ---
    
    def obtener_estadisticas_usuario(self, id_cuenta):
        df = self.cargar_datos()
        if df is None or df.empty: return None
        datos_cuenta = df[df['id_cuenta'] == id_cuenta]
        if datos_cuenta.empty: return None
        montos = datos_cuenta['monto'].to_numpy()
        return {
            "Total transacciones": len(montos),
            "Suma total": np.sum(montos),
            "Promedio": np.mean(montos),
            "Desviación estándar": np.std(montos),
            "Percentil 25": np.percentile(montos, 25) if len(montos) > 0 else 0,
            "Percentil 50 (Mediana)": np.percentile(montos, 50) if len(montos) > 0 else 0,
            "Percentil 75": np.percentile(montos, 75) if len(montos) > 0 else 0
        }

    def obtener_dashboard_admin(self):
        df = self.cargar_datos()
        if df is None or df.empty: return {}
        
        df['fecha'] = df['fecha_hora'].dt.date
        dias_pico = df['fecha'].value_counts().head(5).to_string()
        
        depositos = df[df['tipo'] == 'DEPOSITO']
        top_depositos = depositos.groupby('id_cuenta')['monto'].sum().nlargest(10).to_string() if not depositos.empty else "Sin datos"
        
        gastos = df[df['tipo'] == 'RETIRO']
        top_gastos = gastos.groupby('id_cuenta')['monto'].sum().nlargest(10).to_string() if not gastos.empty else "Sin datos"
        
        return {
            'dias_pico': dias_pico,
            'top_depositos': top_depositos,
            'top_gastos': top_gastos
        }

    def reportar_z_score(self):
        df = self.cargar_datos()
        if df is None or df.empty: return "Sin datos"
        anomalias = []
        for id_cuenta in df['id_cuenta'].unique():
            anomalia = self.detectar_zscore(id_cuenta)
            if len(anomalia) > 0:
                anomalias.append(anomalia)
        if not anomalias: return "No se detectaron anomalías Z-Score."
        return pd.concat(anomalias).to_string()

    def reportar_structuring(self):
        anomalias = self.detectar_structuring()
        if len(anomalias) == 0: return "No se detectaron anomalías de Structuring."
        return anomalias.to_string()

    def reportar_actividad_nocturna(self):
        df = self.cargar_datos()
        if df is None or df.empty: return "Sin datos"
        anomalias = []
        for id_cuenta in df['id_cuenta'].unique():
            anomalia = self.detectar_actividad_nocturna(id_cuenta)
            if len(anomalia) > 0:
                anomalias.append(anomalia)
        if not anomalias: return "No se detectaron anomalías nocturnas."
        return pd.concat(anomalias).to_string()

    def generar_visualizaciones(self):
        try:
            import matplotlib.pyplot as plt
            out_dir = os.path.join("banksystemapp", "outputs", "plots")
            os.makedirs(out_dir, exist_ok=True)
            df = self.cargar_datos()
            if df is None or df.empty: return
            
            plt.figure()
            df['fecha_hora'].dt.date.value_counts().sort_index().plot()
            plt.title("Serie temporal: Transacciones por Día")
            plt.savefig(os.path.join(out_dir, "serie_temporal.png"))
            plt.close()
        except ImportError:
            print("AVISO: matplotlib no está instalado. Ejecute 'pip install matplotlib' para generar gráficos.")

    def obtener_metricas_grafo(self):
        try:
            import networkx as nx
            if not os.path.exists(self.ruta_tr): return "Sin datos de transferencias."
            dft = pd.read_csv(self.ruta_tr)
            if dft.empty: return "No hay transferencias."
            G = nx.from_pandas_edgelist(dft, 'id_origen', 'id_destino', create_using=nx.DiGraph())
            return f"Grafo generado exitosamente.\nNodos identificados: {G.number_of_nodes()}\nAristas (Transferencias): {G.number_of_edges()}"
        except ImportError:
            return "AVISO: networkx no está instalado. Ejecute 'pip install networkx' para usar grafos."
