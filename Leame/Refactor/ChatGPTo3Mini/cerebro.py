"""
Módulo principal que actúa como la "cabeza" del programa.
"""

import os
from explorador import generar_arbol_principal
from registro import loggingprint

def obtener_input(mensaje: str) -> str:
    """
    Obtiene y valida la entrada del usuario.

    Args:
        mensaje (str): Mensaje para solicitar la entrada.

    Returns:
        str: Entrada del usuario.
    """
    entrada = input(mensaje).strip()
    while not entrada:
        loggingprint("La entrada no puede estar vacía. Inténtalo de nuevo.")
        entrada = input(mensaje).strip()
    return entrada

def main() -> None:
    """
    Función principal que ejecuta el flujo del programa.
    """
    try:
        nombre_proyecto = obtener_input("Ingrese el Nombre del Proyecto: ")
        operador = obtener_input("Ingrese el Operador: ")
        carpeta_madre = obtener_input("Ingrese la ruta de la Carpeta Madre (con todas las subcarpetas): ")

        if not os.path.isdir(carpeta_madre):
            loggingprint("La ruta especificada no es una carpeta válida.")
            return

        archivo_salida = "informe_estructura_proyecto.txt"
        arbol = generar_arbol_principal(carpeta_madre)

        with open(archivo_salida, "w", encoding="utf-8") as f:
            f.write(f"Proyecto: {nombre_proyecto}\n")
            f.write(f"Operador: {operador}\n\n")
            f.write("Estructura de carpetas y archivos:\n")
            for linea in arbol:
                f.write(linea + "\n")

        loggingprint(f"Estructura generada correctamente en '{archivo_salida}'.")
    except Exception as e:
        loggingprint(f"Se produjo un error: {e}")

if __name__ == "__main__":
    main()
