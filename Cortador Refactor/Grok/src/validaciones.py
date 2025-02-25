import arcpy
import logging
from pathlib import Path
from typing import Tuple

def validar_entradas(gdb_entrada: str, clip_features: str) -> Tuple[bool, str]:
    """Valida las entradas del usuario.

    Args:
        gdb_entrada: Ruta de la GDB de entrada.
        clip_features: Ruta del shapefile de recorte.

    Returns:
        Tuple con (éxito, mensaje de error si aplica).
    """
    if not gdb_entrada or not clip_features:
        return False, "Las rutas no pueden estar vacías."
    if not arcpy.Exists(gdb_entrada):
        return False, f"La GDB de entrada no existe: {gdb_entrada}"
    if not arcpy.Exists(clip_features):
        return False, f"El shapefile de recorte no existe: {clip_features}"
    return True, ""