import os
import time
import arcpy
from geoprocesamiento import clip_layers
from utilidades import get_unique_gdb_name, delete_unwanted_files
from logging_utils import logging_print
from config import CONFIG

__author__ = "Jorge Vallejo @OnfeVS"
__version__ = "1.0.0"
__date__ = "2024-01-28"

def main() -> None:
    """
    Función principal para ejecutar el script de recorte de GDB.
    
    Se solicitan las rutas de entrada al usuario, se valida la existencia de la GDB y el shapefile,
    se crea una GDB de salida con nombre único y se ejecuta el recorte de capas.
    """
    logging_print("=== Script para Recortar GDB con un Área de Recorte ===")
    logging_print(f"=== Versión: {__version__} | Autor: {__author__} ===")

    start_time = time.time()

    # Solicitar y validar rutas de entrada
    gdb_input: str = input("Ingrese la ruta de la GDB de entrada: ").strip()
    clip_features: str = input("Ingrese la ruta del shapefile para el recorte: ").strip()

    if not arcpy.Exists(gdb_input):
        logging_print("Error: La GDB de entrada no existe.", nivel="error")
        return
    if not arcpy.Exists(clip_features):
        logging_print("Error: El shapefile de recorte no existe.", nivel="error")
        return

    output_folder: str = os.path.dirname(gdb_input)
    gdb_output: str = get_unique_gdb_name(output_folder)

    # Crear la GDB de salida
    try:
        arcpy.CreateFileGDB_management(output_folder, os.path.basename(gdb_output))
        logging_print(f"Nueva GDB creada: {gdb_output}")
    except arcpy.ExecuteError as e:
        logging_print(f"Error creando la GDB de salida: {e}", nivel="error")
        return

    # Ejecutar el recorte de capas y eliminar archivos no deseados
    clip_layers(gdb_input, clip_features, gdb_output)
    delete_unwanted_files(gdb_output)

    elapsed_time = time.time() - start_time
    tiempo_estandar = CONFIG.get("tiempo_estandar", 1800)
    time_saved_percentage = round(100 * (1 - (elapsed_time / tiempo_estandar)))

    logging_print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos.")
    logging_print("========================")
    logging_print("=== Créditos ===")
    logging_print(f"Realizado por: {__author__}")
    logging_print("Contacto: @OnfeVS")
    logging_print("========================")
    logging_print(f"Acabas de ahorrarte un {time_saved_percentage}% de tiempo usando el script, ya que esta tarea manual normalmente tomaría + de 30 minutos.")

if __name__ == "__main__":
    main()


