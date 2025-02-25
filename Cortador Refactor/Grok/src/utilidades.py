import arcpy
import logging
from pathlib import Path
from typing import Optional

def generar_nombre_gdb_unico(base_folder: Path, prefijo: str) -> str:
    """Genera un nombre único para la GDB de salida.

    Args:
        base_folder: Carpeta base para la GDB.
        prefijo: Prefijo para el nombre de la GDB.

    Returns:
        Ruta completa de la GDB única.
    """
    contador = 1
    while True:
        nombre = f"{prefijo}_{contador}.gdb"
        ruta = base_folder / nombre
        if not arcpy.Exists(str(ruta)):
            return str(ruta)
        contador += 1

def eliminar_archivos_temp(gdb_path: str) -> None:
    """Elimina archivos temporales de la GDB.

    Args:
        gdb_path: Ruta de la GDB.
    """
    templates = ["GDB_EditingTemplates", "GDB_EditingTemplateRelationships"]
    for template in templates:
        ruta = f"{gdb_path}/{template}"
        if arcpy.Exists(ruta):
            arcpy.Delete_management(ruta)
            logging.info(f"Archivo temporal eliminado: {ruta}")