import os, time

class MenuBase:
    def __init__(self):
        pass
    
    def limpiar_consola(self):
        """
        Limpia la consola de la terminal
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausa(self, segundos=2):
        """
        Pausa la ejecución del programa durante el tiempo indicado
        """
        time.sleep(segundos)
    
    def mostrar_encabezado(self, titulo, cantidad_elementos, simbolo="=", es_salto_de_linea=False):
        """
        Muestra un encabezado con el título y el simbolo indicando el nivel de indentación
        """
        if es_salto_de_linea:
            print()
        print(simbolo * cantidad_elementos)
        print(f"\t{titulo}")
        print(simbolo * cantidad_elementos)
    
    def pedir_opcion(self, opciones=None, mensaje="Elija una opción: "):
        """
        Pedir una opción al usuario
        """
        opcion = input(mensaje)
        opcion = opcion.lower()
        if opciones:
            num_opciones_validas = [str(i+1) for i in range(len(opciones))]
            if opcion not in num_opciones_validas:
                raise ValueError(f"Opción no válida. Ingrese un número entre 1 y {len(opciones)}")
        return opcion
    
    def continuar(self):
        """
        Muestra un mensaje de continuación y espera a que el usuario pulse ENTER
        """
        input("\nPulse ENTER para continuar...")
    
    def salir(self, mensaje="Cerrando sesión..."):
        """
        Salir de un menu
        """
        print("-" * 43)
        print(mensaje)
        self.pausa(2)
        self.limpiar_consola()