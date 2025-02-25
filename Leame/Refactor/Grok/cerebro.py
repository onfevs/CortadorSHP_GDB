import os
from typing import Optional
from manos import generar_arbol_principal
from voz import obtener_entrada_usuario, log_info, log_error

def main() -> None:
    """Punto de entrada principal del programa."""
    # Solicitar datos
    nombre_proyecto = obtener_entrada_usuario("Ingrese el Nombre del Proyecto: ")
    if not nombre_proyecto:
        return

    operador = obtener_entrada_usuario("Ingrese el Operador: ")
    if not operador:
        return

    carpeta_madre = obtener_entrada_usuario("Ingrese la ruta de la Carpeta Madre: ")
    if not carpeta_madre or not os.path.isdir(carpeta_madre):
        log_error(f"La ruta '{carpeta_madre}' no es una carpeta válida.")
        return

    # Generar árbol
    arbol = generar_arbol_principal(carpeta_madre)
    archivo_salida = "informe_estructura_proyecto.txt"

    # Escribir informe con context manager
    try:
        with open(archivo_salida, "w", encoding="utf-8") as f:
            f.write(f"Proyecto: {nombre_proyecto}\n")
            f.write(f"Operador: {operador}\n\n")
            f.write("Estructura de carpetas y archivos:\n")
            f.writelines(linea + "\n" for linea in arbol)
        log_info(f"Estructura generada correctamente en '{archivo_salida}'.")
    except IOError as e:
        log_error(f"Error al escribir el archivo: {str(e)}")

if __name__ == "__main__":
    main()