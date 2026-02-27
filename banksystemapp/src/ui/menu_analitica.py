from .menu_base import MenuBase
from ..services.analysis_service import AnalisisService

class MenuAnalitica(MenuBase):
    def __init__(self):
        super().__init__()
        self.analisis_service = AnalisisService()
        self.opciones = [
            '1. Estadísticas por usuario',
            '2. Estadísticas de administrador',
            '3. Detalle de anomalías',
            '4. Gráficos de análisis',
            '5. Grafos con transferencias',
            '6. Regresar'
        ]
    
    def ejecutar(self):
        while True:
            self.mostrar_encabezado("Analisis de datos", 48, simbolo="-", es_salto_de_linea=True)
            for opcion in self.opciones:
                print(f"\t{opcion}")
            
            try:
                seleccion = self.pedir_opcion(self.opciones)
                if seleccion == '1':
                    self.estadisticas_por_usuario()
                elif seleccion == '2':
                    self.estadisticas_administrador()
                elif seleccion == '3':
                    self.detalle_analisis()
                elif seleccion == '4':
                    self.graficos_analisis()
                elif seleccion == '5':
                    self.grafos_transferencias()
                elif seleccion == '6':
                    self.limpiar_consola()
                    break 
            except Exception as e:
                print(f"Error: {e}")
                self.pausa(2)
                self.limpiar_consola()
    
    def estadisticas_por_usuario(self):
        """Muestra estadísticas individuales: total depósitos, promedio, desviación y percentiles."""
        self.mostrar_encabezado("Estadísticas por usuario", 40, simbolo="-", es_salto_de_linea=True)
        
        todas_estadisticas = self.analisis_service.obtener_estadisticas_completas()
        
        if not todas_estadisticas:
            print("No se encontraron datos para mostrar.")
            self.continuar()
            self.limpiar_consola()
            return
        self._imprimir_tabla_estadisticas(todas_estadisticas)
        
        print("\n")
        id_cuenta = input("Ingrese el ID de la cuenta a analizar (ej. C001) o presione ENTER para salir: ").strip().upper()
        
        if id_cuenta:
            estadisticas_filtrada = self.analisis_service.obtener_estadisticas_completas(id_cuenta)
            if estadisticas_filtrada:
                self._imprimir_tabla_estadisticas(estadisticas_filtrada)
            else:
                print(f"No se encontraron datos para la cuenta {id_cuenta}.")
        
        self.continuar()
        self.limpiar_consola()
    
    def _imprimir_tabla_estadisticas(self, datos):
        """Imprime los diccionarios en un formato de tabla alineado."""
        encabezados = ["ID Cuenta", "DUI Propietario", "Total Depósitos", "Promedio Diario", "Desviación", "p50", "p90", "p99", "Depositos/Gastos"]
        
        formato_fila = "{:<10} {:<15} {:<18} {:<18} {:<15} {:<10} {:<10} {:<10} {:<18}"
        
        print(formato_fila.format(*encabezados))
        print("-" * 130)
        for fila in datos:
            print(formato_fila.format(
                fila['ID Cuenta'],
                fila['DUI Propietario'],
                fila['Total Depositos'],
                fila['Promedio Diario'],
                fila['Desviacion'],
                fila['p50'],
                fila['p90'],
                fila['p99'],
                fila['Depositos/Gastos']
            ))
    
    def estadisticas_administrador(self):
        """Muestra el Dashboard de administrador: top días pico y top cuentas [cite: 64-71]."""
        self.mostrar_encabezado("Estadísticas de administrador", 45, simbolo="-", es_salto_de_linea=True)
        
        dashboard = self.analisis_service.obtener_dashboard_admin()
        
        print("\n--- TOP 5 DÍAS PICO ---")
        print(dashboard.get('dias_pico', 'Sin datos'))
        
        print("\n--- TOP 10 CUENTAS (DEPÓSITOS) ---")
        print(dashboard.get('top_depositos', 'Sin datos'))
        
        print("\n--- TOP 10 CUENTAS (GASTOS) ---")
        print(dashboard.get('top_gastos', 'Sin datos'))
        
        self.continuar()
        self.limpiar_consola()
    
    def detalle_analisis(self):
        """Reporta las 3 anomalías: Z-score, Structuring y Actividad Nocturna [cite: 72-74, 79, 85]."""
        self.mostrar_encabezado("Detalle de anomalías", 38, simbolo="-", es_salto_de_linea=True)
        
        print("[1] Anomalías de Monto (Z-Score > 3):")
        print(self.analisis_service.reportar_z_score())
        
        print("\n[2] Depósitos Partidos (Structuring):")
        print(self.analisis_service.reportar_structuring())
        
        print("\n[3] Actividad Nocturna Inusual (21:00 - 04:00):")
        print(self.analisis_service.reportar_actividad_nocturna())
        
        self.continuar()
        self.limpiar_consola()
    
    def graficos_analisis(self):
        """Genera y exporta archivos PNG a outputs/plots/ [cite: 94-98]."""
        self.mostrar_encabezado("Generando gráficos de análisis", 40, simbolo="-", es_salto_de_linea=True)
        
        # Matplotlib y Seaborn deben usarse aquí [cite: 5, 6]
        print("Procesando: Serie temporal, Heatmap, Boxplot y Scatter plot...")
        self.analisis_service.generar_visualizaciones()
        print("✓ Archivos guardados en banksystemapp/outputs/plots/")
        
        self.continuar()
        self.limpiar_consola()
    
    def grafos_transferencias(self):
            """Permite obtener los gráficos de transferencias[cite: 192]."""
            self.mostrar_encabezado("Módulo de Grafos con Transferencias", 42, simbolo="-", es_salto_de_linea=True)
            
            print("Calculando métricas de red, centralidad y comunidades...")
            # Llamada al servicio que acabamos de programar
            resultado = self.analisis_service.obtener_metricas_grafo()
            
            print(resultado)
            print("\n[✓] El gráfico visual ha sido generado en: banksystemapp/outputs/plots/grafo_transferencias.png")
            
            self.continuar()
            self.limpiar_consola()