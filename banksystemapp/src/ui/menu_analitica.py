from ..services.analysis_services import AnalisisService
from .menu_base import MenuBase

class MenuAnalitica(MenuBase):
    def __init__(self):
        super().__init__()
        self.analisis_service = AnalisisService()
        self.opciones = [
            '1. Estadísticas por usuario',
            '2. Estadísticas de administrador',
            '3. Detalle de anomalías',
            '4. Graficos de análisis',
            '5. Modulo de grafos con transferencias',
            '6. Regresar'
        ]
    
    def ejecutar(self):
        """
        Bucle principal del menu de analítica
        """
        while True:
            self.mostrar_encabezado("Ejecución de modulo de analitica", 48, simbolo="-", es_salto_de_linea=True)
            
            try:
                opciones = [
                    '1. Estadísticas por usuario',
                    '2. Estadísticas de administrador',
                    '3. Detalle de anomalías',
                    '4. Graficos de análisis',
                    '5. Modulo de grafos con transferencias',
                    '6. Regresar'
                ]
                for opcion in opciones:
                    print(f"\t{opcion}")
                
                seleccion = self.pedir_opcion(opciones)
                
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
                    break  # Solo regresa al menú 
                else:
                    print("Opción no válida. Intente nuevamente")
                    self.pausa(2)
                    self.limpiar_consola()
            except Exception as e:
                print(f"Error: {e}")
                self.continuar()
                self.limpiar_consola()
    
    # =================================================================
    # -------------- EJECUCIÓN DEL MODULO DE ANALITICA ----------------
    # =================================================================
    def estadisticas_por_usuario(self):
        """
        Permite obtener las estadísticas de usuarios
        """
        self.mostrar_encabezado("Estadísticas por usuario", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def estadisticas_administrador(self):
        """
        Permite obtener las estadísticas de administradores
        """
        self.mostrar_encabezado("Estadísticas de administrador", 45, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def detalle_analisis(self):
        """
        Permite obtener los detalles de las anomalías
        """
        self.mostrar_encabezado("Detalle de anomalías", 38, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def graficos_analisis(self):
        """
        Permite obtener los gráficos de análisis
        """
        self.mostrar_encabezado("Gráficos de análisis", 40, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()
    
    def grafos_transferencias(self):
        """
        Permite obtener los gráficos de transferencias
        """
        self.mostrar_encabezado("Gráficos de transferencias", 42, simbolo="-", es_salto_de_linea=True)
        print("En construcción...")
        self.continuar()
        self.limpiar_consola()