import arcpy
import logging
from pathlib import Path
from typing import List

def obtener_datasets(gdb: str) -> List[str]:
    """Obtiene todos los feature datasets recursivamente."""
    arcpy.env.workspace = gdb
    datasets = []
    try:
        datasets.extend(arcpy.ListDatasets("", "Feature"))
        for ds in datasets[:]:  # Copia para evitar modificación durante iteración
            datasets.extend(arcpy.ListDatasets(f"{ds}/*", "Feature"))
    except arcpy.ExecuteError as e:
        logging.error(f"Error al listar datasets: {e}")
    return datasets

def tiene_interseccion(fc: str, clip_features: str) -> bool:
    """Verifica si una capa tiene intersección con el área de recorte."""
    try:
        result = arcpy.SelectLayerByLocation_management(fc, "INTERSECT", clip_features)
        return int(arcpy.GetCount_management(result)[0]) > 0
    except arcpy.ExecuteError:
        return False  # Silenciamos logging aquí para evitar overhead en bucles

def esta_vacia(fc: str) -> bool:
    """Verifica si una capa está vacía."""
    try:
        return int(arcpy.GetCount_management(fc)[0]) == 0
    except arcpy.ExecuteError:
        return True  # Silenciamos logging para optimizar

def recortar_capas(gdb_entrada: str, clip_features: str, gdb_salida: str) -> None:
    """Procesa y recorta capas y datasets con un shapefile."""
    arcpy.env.workspace = gdb_entrada
    logging.info("Iniciando recorte de capas...")

    # Procesar capas raíz
    for fc in arcpy.ListFeatureClasses():
        if tiene_interseccion(fc, clip_features):
            salida = f"{gdb_salida}/{Path(fc).name}"
            arcpy.Clip_analysis(fc, clip_features, salida)
            if esta_vacia(salida):
                arcpy.Delete_management(salida)
            # Logging solo al final en main.py

    # Procesar datasets
    datasets = obtener_datasets(gdb_entrada)
    if not datasets:
        logging.info("No se encontraron datasets.")
        return

    for fds in datasets:
        desc = arcpy.Describe(fds)
        salida_fds = f"{gdb_salida}/{fds}"
        tiene_datos = False

        for fc in arcpy.ListFeatureClasses("", "", fds):
            if tiene_interseccion(fc, clip_features):
                if not tiene_datos:
                    arcpy.CreateFeatureDataset_management(gdb_salida, fds, desc.spatialReference)
                    tiene_datos = True
                salida = f"{salida_fds}/{Path(fc).name}"
                arcpy.Clip_analysis(fc, clip_features, salida)
                if esta_vacia(salida):
                    arcpy.Delete_management(salida)
        # Logging solo al final

    # Procesar tablas
    for table in arcpy.ListTables():
        if table.endswith("TB") and not esta_vacia(table):
            arcpy.Copy_management(table, f"{gdb_salida}/{table}")
    logging.info("Recorte de capas finalizado.")

def procesar_capa(fc: str, clip_features: str, gdb_salida: str) -> None:
    """Procesa una capa individual (no usado en esta versión optimizada)."""
    pass  # Eliminado para evitar redundancia con recortar_capas

def procesar_dataset(fds: str, clip_features: str, gdb_salida: str, gdb_entrada: str) -> None:
    """Procesa un feature dataset (no usado en esta versión optimizada)."""
    pass  # Eliminado para evitar redundancia con recortar_capas
