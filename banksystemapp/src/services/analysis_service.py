import numpy as np
import pandas as pd
import os
from ..repositories.cuentas.transferencia_repository import TransferenciaRepository

class AnalisisService:
    def __init__(self):
        self.ruta_tx = os.path.join("banksystemapp", "data", "transacciones.csv")
        self.ruta_tr = os.path.join("banksystemapp", "data", "transferencias.csv")
        self.ruta_cuentas = os.path.join("banksystemapp", "data", "cuentas.csv")
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
    
    def obtener_estadisticas_completas(self, id_cuenta_filtro=None):
        """Calcula las estadísticas para todas las cuentas o una específica 
        si se proporciona el filtro."""
        df_tx = self.cargar_datos()
        ruta_cuentas = os.path.join("banksystemapp", "data", "cuentas.csv")
        
        if not os.path.exists(ruta_cuentas): return []
        
        df_cuentas = pd.read_csv(ruta_cuentas)
        resultados = []
        
        for _, cuenta in df_cuentas.iterrows():
            id_cuenta = cuenta['id_cuenta']
            if id_cuenta_filtro and id_cuenta != id_cuenta_filtro: continue
            
            dui = cuenta['dui_propietario']
            if df_tx is not None and not df_tx.empty: 
                tx_cuenta = df_tx[df_tx['id_cuenta'] == id_cuenta].copy()
            else:
                tx_cuenta = pd.DataFrame()
            
            if not tx_cuenta.empty:
                depositos = tx_cuenta[tx_cuenta['tipo'] == 'DEPOSITO']['monto'].to_numpy()
                total_depositos = np.sum(depositos) if len(depositos) > 0 else 0.0
                gastos = tx_cuenta[tx_cuenta['tipo'] == 'RETIRO']['monto'].to_numpy()
                total_gastos = np.sum(gastos) if len(gastos) > 0 else 0.0

                if total_gastos == 0:
                    ratio_str = "Inf" if total_depositos > 0 else "0.00"
                else:
                    ratio_str = f"{total_depositos / total_gastos:.2f}"
                montos = tx_cuenta['monto'].to_numpy() # Arreglo de montos para estadísticas de cuenta
                
                # Promedio diario
                tx_cuenta['fecha'] = tx_cuenta['fecha_hora'].dt.date
                dias_unicos = tx_cuenta['fecha'].nunique()
                promedio_diario = np.sum(montos) / dias_unicos if dias_unicos > 0 else 0.0
                
                # Desviación estándar y percentiles
                desviacion = np.std(montos)
                p50 = np.percentile(montos, 50)
                p90 = np.percentile(montos, 90)
                p99 = np.percentile(montos, 99)
            else:
                total_depositos = 0.0
                promedio_diario = 0.0
                desviacion = 0.0
                p50, p90, p99 = 0.0, 0.0, 0.0
                ratio_str = "0.00"
            
            resultados.append({
                "ID Cuenta": id_cuenta,
                "DUI Propietario": dui,
                "Total Depositos": f"${total_depositos:,.2f}",
                "Promedio Diario": f"${promedio_diario:,.2f}",
                "Desviacion": f"${desviacion:,.2f}",
                "p50": f"${p50:,.2f}",
                "p90": f"${p90:,.2f}",
                "p99": f"${p99:,.2f}",
                "Depositos/Gastos": ratio_str
            })
        return resultados

    def obtener_dashboard_admin(self):
        """Genera las métricas generales del banco para el dashboard del administrador"""
        df_tx = self.cargar_datos()
        if df_tx is None or df_tx.empty: return None
        
        # Transacciones por día y días pico (top 5) 
        df_tx['fecha'] = df_tx['fecha_hora'].dt.date
        tx_por_dia = df_tx.groupby('fecha').size()
        dias_pico = tx_por_dia.nlargest(5).to_dict()
        
        # Total diario del banco (Depositos, Gastos, Neto)
        total_diario_tipo = df_tx.groupby(['fecha', 'tipo'])['monto'].sum().unstack(fill_value=0)
        
        # Si no se encuentran datos, se agregan valores iniciales para evitar errores
        if 'DEPOSITO' not in total_diario_tipo.columns:
            total_diario_tipo['DEPOSITO'] = 0.0
        if 'RETIRO' not in total_diario_tipo.columns:
            total_diario_tipo['RETIRO'] = 0.0
        total_diario_tipo['NETO'] = total_diario_tipo['DEPOSITO'] - total_diario_tipo['RETIRO']
        
        # Ultimos 5 días de actividad
        total_diario = total_diario_tipo.tail(5).sort_index(ascending=False).to_dict(orient='index')
        
        # Top 10 cuentas por depósitos y gastos
        depositos = df_tx[df_tx['tipo'] == 'DEPOSITO']
        top_depositos = depositos.groupby('id_cuenta')['monto'].sum().nlargest(10).to_dict()
        
        gastos = df_tx[df_tx['tipo'] == 'RETIRO']
        top_gastos = gastos.groupby('id_cuenta')['monto'].sum().nlargest(10).to_dict()
        
        total_zscore = 0
        total_nocturna = 0
        
        for id_cuenta in df_tx['id_cuenta'].unique():
            anom_z = self.detectar_zscore(id_cuenta)
            total_zscore += len(anom_z) if anom_z is not None and not isinstance(anom_z, list) else 0
            
            anom_n = self.detectar_actividad_nocturna(id_cuenta)
            total_nocturna += len(anom_n) if anom_n is not None and not isinstance(anom_n, list) else 0
        
        anom_s = self.detectar_structuring()
        total_structuring = len(anom_s) if anom_s is not None and not isinstance(anom_s, list) else 0
        
        resumen_anomalias = {
            "Z-Score (Montos Atípicos)": total_zscore,
            "Actividad Nocturna Inusual": total_nocturna,
            "Structuring (Depósitos Partidos)": total_structuring
        }
        
        return {
            'dias_pico': dias_pico,
            'total_diario_banco': total_diario,
            'top_depositos': top_depositos,
            'top_gastos': top_gastos,
            'resumen_anomalias': resumen_anomalias
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
        """Genera y exporta las visualizaciones de los datos"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            out_dir = self.ruta_plots
            os.makedirs(out_dir, exist_ok=True)
            
            df_tx = self.cargar_datos()
            if df_tx is None or df_tx.empty: 
                print("No hay datos suficientes para generar los gráficos.")
                return
            
            ruta_cuentas = self.ruta_cuentas
            df_cuentas = pd.read_csv(ruta_cuentas)
            
            # Combinar transacciones y cuentas para obtener el tipo de cuenta disponible
            df_merged = df_tx.merge(df_cuentas[['id_cuenta', 'tipo']], on='id_cuenta', how='left')
            df_merged.rename(columns={'tipo_x': 'tipo_tx', 'tipo_y': 'tipo_cuenta'}, inplace=True)
            
            # -----------------------------------------------------------------------
            # Serie temporal del total de depositos, gastos y neto del banco por día
            # -----------------------------------------------------------------------
            plt.figure(figsize=(10, 6))
            df_merged['fecha'] = df_merged['fecha_hora'].dt.date
            
            # Agrupamos por fecha y tipo de transacción
            diario = df_merged.groupby(['fecha', 'tipo_tx'])['monto'].sum().unstack(fill_value=0)
            if 'DEPOSITO' not in diario.columns: diario['DEPOSITO'] = 0.0
            if 'RETIRO' not in diario.columns: diario['RETIRO'] = 0.0
            # Calculamos el neto
            diario['NETO'] = diario['DEPOSITO'] - diario['RETIRO']
            
            plt.plot(diario.index, diario['DEPOSITO'], marker='o', label='Depositos', color='green', linewidth=2)
            plt.plot(diario.index, diario['RETIRO'], marker='o', label='Retiros', color='red', linewidth=2)
            plt.plot(diario.index, diario['NETO'], marker='o', label='Neto', color='blue', linewidth=2)
            
            plt.title("Serie temporal: Total de depositos del banco por día", fontsize=14, pad=15)
            plt.xlabel("Fecha", fontsize=12)
            plt.ylabel("Monto Total ($)", fontsize=12)
            plt.legend(title='Tipo de movimiento')
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(out_dir, "serie_temporal_depositos.png"))
            plt.close()
            
            # -----------------------------------------------------------
            # Heatmap de actividad (Top 10 cuentas vs Dias de la semana)
            # -----------------------------------------------------------
            plt.figure(figsize=(10, 6))
            # Encontrar las 10 cuentas con más transacciones
            top_cuentas = df_merged['id_cuenta'].value_counts().nlargest(10).index
            df_top = df_merged[df_merged['id_cuenta'].isin(top_cuentas)].copy()
            
            df_top['dia_semana'] = df_top['fecha_hora'].dt.day_name()
            # Ordenar los días de la semana para el heatmap
            dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            
            heatmap_data = df_top.groupby(['id_cuenta', 'dia_semana']).size().unstack(fill_value=0) # Matriz de Cuenta vs Día de la semana
            heatmap_data = heatmap_data.reindex(columns=dias_orden, fill_value=0) # Asegurar el orden correcto de los días
            heatmap_data.columns = dias_espanol # Traducir columnas a español
            
            sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5)
            plt.title("Heatmap: Top 10 cuentas por día de la semana", fontsize=14, pad=15)
            plt.xlabel("Día de la semana", fontsize=12)
            plt.ylabel("ID de Cuenta", fontsize=12)
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig(os.path.join(out_dir, "heatmap_actividad.png"))
            plt.close()
            
            # ----------------------------------------------------
            # Boxplot por segmento (Depositos por tipo de cuenta)
            # ----------------------------------------------------
            plt.figure(figsize=(10, 6))
            depositos = df_merged[df_merged['tipo_tx'] == 'DEPOSITO']
            
            sns.boxplot(x='tipo_cuenta', y='monto', data=depositos, hue='tipo_cuenta', palette='Set2', legend=False)
            plt.title("Boxplot: Depositos por tipo de cuenta", fontsize=14, pad=15)
            plt.xlabel("Tipo de cuenta", fontsize=12)
            plt.ylabel("Monto del deposito ($)", fontsize=12)
            plt.tight_layout()
            plt.savefig(os.path.join(out_dir, "boxplot_depositos.png"))
            plt.close()
            
            # ----------------------------------------------------
            # Scatterplot (Depósitos vs Gastos)
            # ----------------------------------------------------  
            plt.figure(figsize=(10, 6))
            
            # Creamos un pivote con total depositos y retiro por cuenta
            pivote = df_merged.groupby(['id_cuenta', 'tipo_tx'])['monto'].sum().unstack(fill_value=0)
            if 'DEPOSITO' not in pivote.columns: pivote['DEPOSITO'] = 0.0
            if 'RETIRO' not in pivote.columns: pivote['RETIRO'] = 0.0
            
            # Unimos con el tipo de cuenta para colorear por segmento
            scatter_data = pivote.merge(df_cuentas[['id_cuenta', 'tipo']], on='id_cuenta', how='left')
            
            sns.scatterplot(x='DEPOSITO', y='RETIRO', hue='tipo', data=scatter_data, s=150, palette='deep', alpha=0.7, edgecolor='black')
            plt.title("Scatterplot: Depósitos vs Gastos", fontsize=14, pad=15)
            plt.xlabel("Monto Total de Retiros ($)", fontsize=12)
            plt.ylabel("Monto Total de Depositos ($)", fontsize=12)
            plt.legend(title="Tipo de cuenta")
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig(os.path.join(out_dir, "scatterplot_depositos_gastos.png"))
            plt.close()
            
        except ImportError as e:
            print(f"AVISO: Faltan librerias para graficar ({e})")
        except Exception as e:
            print(f"AVISO: Error al generar gráficos ({e})")
    
    
    def obtener_metricas_grafo(self):
            """
            Crea el grafo dirigido y calcula métricas de red.
            """
            try:
                import networkx as nx
                import matplotlib.pyplot as plt
            except ImportError:
                return "AVISO: networkx o matplotlib no están instalados. Ejecute 'pip install networkx matplotlib' para este módulo."
            
            # 1. Cargar todas las transferencias desde el repositorio
            transferencias = self.transferencia_repo.obtener_todas()
            
            # 2. Inicializar el grafo dirigido
            G = nx.DiGraph()
            
            # 3. Construir nodos (cuentas) y aristas (transferencias)
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

            # 4. Calcular métricas mínimas obligatorias
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

            # 6. Generar y guardar la imagen obligatoria
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
            
        # Guardar en la ruta especificada
        os.makedirs(self.ruta_plots, exist_ok=True)
        ruta_archivo = os.path.join(self.ruta_plots, "grafo_transferencias.png")
        plt.savefig(ruta_archivo, bbox_inches='tight')
        plt.close()