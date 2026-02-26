from .menu_base import MenuBase
from ..services.analysis_services import AnalisisService # Asegúrate que el nombre del archivo coincida

class MenuAnalitica(MenuBase):
    def __init__(self):
        super().__init__()
        self.analisis_service = AnalisisService()
        self.opciones = [
            '1. Estadísticas por usuario',
            '2. Estadísticas de administrador',
            '3. Detalle de anomalías',
            '4. Gráficos de análisis',
            '5. Módulo de grafos con transferencias',
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
        """Muestra estadísticas individuales: total depósitos, promedio, desviación y percentiles [cite: 57-63]."""
        self.mostrar_encabezado("Estadísticas por usuario", 40, simbolo="-", es_salto_de_linea=True)
        id_cuenta = input("Ingrese el ID de la cuenta a analizar (ej. C001): ").strip().upper()
        
        # El servicio debe usar NumPy para estos cálculos sin ciclos for [cite: 55]
        stats = self.analisis_service.obtener_estadisticas_usuario(id_cuenta)
        if stats:
            print(f"\nResultados para la cuenta {id_cuenta}:")
            for clave, valor in stats.items():
                print(f" - {clave}: {valor}")
        else:
            print("No se encontraron datos para esa cuenta.")
        
        self.continuar()
        self.limpiar_consola()
    
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
        """Módulo de NetworkX: Métricas de red y comunidades [cite: 103, 109-112]."""
        self.mostrar_encabezado("Módulo de grafos con transferencias", 42, simbolo="-", es_salto_de_linea=True)
        
        # Nodo = account_id, Arista = Transferencia [cite: 105-107]
        print("Calculando In-degree, Out-degree y Centralidad...")
        metricas = self.analisis_service.obtener_metricas_grafo()
        print(metricas)
        
        self.continuar()
        self.limpiar_consola()