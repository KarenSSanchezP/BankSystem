import numpy as np
import pandas as pd
import os
from ..repositories.cuentas.transferencia_repository import TransferenciaRepository

class AnalisisService:
    def __init__(self):
        self.ruta_tx = os.path.join("banksystemapp", "data", "transacciones.csv")
        self.ruta_tr = os.path.join("banksystemapp", "data", "transferencias.csv")
        self.ruta_plots = os.path.join("banksystemapp", "outputs", "plots")
        self.transferencia_repo = TransferenciaRepository()

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
            """
            Crea el grafo dirigido y calcula métricas de red [cite: 247-255].
            """
            try:
                import networkx as nx
                import matplotlib.pyplot as plt
            except ImportError:
                return "AVISO: networkx o matplotlib no están instalados. Ejecute 'pip install networkx matplotlib' para este módulo."
            
            # 1. Cargar todas las transferencias desde el repositorio
            transferencias = self.transferencia_repo.obtener_todas()
            
            # 2. Inicializar el grafo dirigido [cite: 247]
            G = nx.DiGraph()
            
            # 3. Construir nodos (cuentas) y aristas (transferencias) [cite: 248-251]
            for tr in transferencias:
                u, v = tr.id_origen, tr.id_destino
                monto = float(tr.monto)
                
                # Peso acumulado: si ya existe la conexión, sumamos el monto 
                if G.has_edge(u, v):
                    G[u][v]['weight'] += monto
                else:
                    G.add_edge(u, v, weight=monto)
            
            if G.number_of_nodes() == 0:
                return "No hay datos de transferencias suficientes para generar el grafo."

            # 4. Calcular métricas mínimas obligatorias [cite: 252-255]
            # In-degree (Recepción) y Out-degree (Envío) ponderados
            in_degrees = dict(G.in_degree(weight='weight'))
            out_degrees = dict(G.out_degree(weight='weight'))
            
            # Betweenness Centrality: identifica cuentas "puente"
            centrality = nx.betweenness_centrality(G, weight='weight')
            
            # Detección de comunidades o agrupaciones 
            comunidades = list(nx.community.greedy_modularity_communities(G))

            # 5. Formatear resumen para el menú
            resumen = f"--- RESULTADOS DEL ANÁLISIS DE RED ---\n"
            resumen += f"Cuentas analizadas: {G.number_of_nodes()}\n"
            resumen += f"Conexiones únicas: {G.number_of_edges()}\n"
            resumen += f"Grupos/Comunidades detectadas: {len(comunidades)}\n\n"
            
            # Encontrar el mayor "Hub" (la cuenta que más dinero envía)
            max_hub = max(out_degrees, key=out_degrees.get)
            resumen += f"Mayor emisor (Hub): {max_hub} (${out_degrees[max_hub]:,.2f})\n"
            
            # Encontrar la cuenta más central (puente)
            max_bridge = max(centrality, key=centrality.get)
            resumen += f"Cuenta puente (Centralidad): {max_bridge}\n"

            # 6. Generar y guardar la imagen obligatoria [cite: 245]
            self._visualizar_grafo(G)
            
            return resumen

    def _visualizar_grafo(self, G):
        """Genera el archivo PNG con títulos y etiquetas ."""
        import matplotlib.pyplot as plt
        import networkx as nx
        plt.figure(figsize=(12, 10))
        # Layout para organizar los nodos
        pos = nx.spring_layout(G, k=0.5, seed=42)
            
        # Dibujar nodos y etiquetas
        nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='orange', alpha=0.9)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
            
        # Dibujar aristas con flechas de dirección
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.4, edge_color='blue', arrows=True)
            
        # Etiquetas de peso (montos transferidos) en las aristas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        # Formateamos los números a moneda sin decimales para no saturar la imagen
        edge_labels_fmt = {k: f"${v:,.0f}" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_fmt, font_size=7)

        plt.title("Grafo Dirigido de Transferencias Bancarias\n(Nodos: Cuentas | Aristas: Flujo Acumulado)", size=15)
        plt.axis('off')
            
        # Guardar en la ruta especificada [cite: 237, 245]
        os.makedirs(self.ruta_plots, exist_ok=True)
        ruta_archivo = os.path.join(self.ruta_plots, "grafo_transferencias.png")
        plt.savefig(ruta_archivo, bbox_inches='tight')
        plt.close()