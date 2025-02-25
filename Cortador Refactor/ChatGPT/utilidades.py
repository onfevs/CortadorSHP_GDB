import os
import arcpy
from logging_utils import logging_print

def get_unique_gdb_name(base_folder: str) -> str:
    """
    Genera un nombre único para la GDB de salida siguiendo el formato CartoBase_1, CartoBase_2, etc.
    
    Args:
        base_folder (str): Carpeta base donde se creará la GDB.
        
    Returns:
        str: Ruta completa de la GDB única.
    """
    counter = 1
    while True:
        gdb_name = f"CartoBase_{counter}.gdb"
        gdb_path = os.path.join(base_folder, gdb_name)
        if not arcpy.Exists(gdb_path):
            return gdb_path
        counter += 1

def delete_unwanted_files(gdb_path: str) -> None:
    """
    Elimina archivos no deseados que se crean automáticamente en la GDB.
    
    Args:
        gdb_path (str): Ruta de la GDB donde se eliminarán los archivos.
    """
    try:
        templates = ["GDB_EditingTemplates", "GDB_EditingTemplateRelationships"]
        for template in templates:
            template_path = os.path.join(gdb_path, template)
            if arcpy.Exists(template_path):
                arcpy.Delete_management(template_path)
                logging_print(f"Archivo eliminado: {template_path}", nivel="debug")
    except arcpy.ExecuteError as e:
        logging_print(f"Error eliminando archivos no deseados: {e}", nivel="error")

