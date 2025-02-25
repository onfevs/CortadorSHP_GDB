import logging
import time
from pathlib import Path
import arcpy
from configuracion import Configuracion
from manejo_gdb import recortar_capas
from utilidades import generar_nombre_gdb_unico, eliminar_archivos_temp
from validaciones import validar_entradas

__author__ = "Jorge Vallejo @OnfeVS"
__version__ = "1.0.0"

def main() -> None:
    """Función principal para ejecutar el script de recorte de GDB."""
    config = Configuracion()
    logging.info(f"Script iniciado | Versión: {__version__} | Autor: {__author__}")

    inicio = time.time()

    gdb_entrada = input("Ingrese la ruta de la GDB de entrada: ").strip()
    clip_features = input("Ingrese la ruta del shapefile para el recorte: ").strip()

    valido, mensaje = validar_entradas(gdb_entrada, clip_features)
    if not valido:
        logging.error(mensaje)
        return

    carpeta_salida = Path(gdb_entrada).parent
    if not carpeta_salida.is_dir():
        logging.error(f"La carpeta de salida no existe: {carpeta_salida}")
        return
    
    gdb_salida = generar_nombre_gdb_unico(carpeta_salida, config.obtener_prefijo_gdb())
    try:
        arcpy.CreateFileGDB_management(str(carpeta_salida), Path(gdb_salida).name)
    except arcpy.ExecuteError as e:
        logging.error(f"Error al crear la GDB: {e}")
        return

    arcpy.env.overwriteOutput = True
    recortar_capas(gdb_entrada, clip_features, gdb_salida)
    eliminar_archivos_temp(gdb_salida)

    tiempo_total = time.time() - inicio
    tiempo_manual = config.obtener_tiempo_manual()
    ahorros = round(100 * (1 - (tiempo_total / tiempo_manual)))

    logging.info(f"Proceso completado en {tiempo_total:.2f} segundos")
    logging.info(f"Ahorro de tiempo estimado: {ahorros}%")
    logging.info(f"Créditos: {__author__} | Contacto: @OnfeVS")

if __name__ == "__main__":
    main()
