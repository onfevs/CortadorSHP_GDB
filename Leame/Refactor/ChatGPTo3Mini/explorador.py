"""
Módulo que contiene funciones para explorar directorios y generar una estructura de árbol.
"""

import os
from typing import List
from configuracion import EXCLUDED_EXTS, DESCRIPTIONS

def listar_contenido(ruta: str, prefijo: str, no_recursion: bool = False) -> List[str]:
    """
    Lista el contenido de un directorio en forma de árbol.

    Args:
        ruta (str): Ruta del directorio.
        prefijo (str): Prefijo para formatear la salida.
        no_recursion (bool, optional): Si es True, no desciende en subdirectorios. Defaults to False.

    Returns:
        List[str]: Lista de líneas representando la estructura de árbol.
    """
    lineas: List[str] = []
    try:
        with os.scandir(ruta) as it:
            items = sorted([entry for entry in it], key=lambda e: e.name.lower())
    except PermissionError:
        return [prefijo + "└── [Sin permisos]"]

    # Filtrar archivos por extensión
    filtered_items = []
    for entry in items:
        if entry.is_file():
            ext = os.path.splitext(entry.name)[1].lower()
            if ext in EXCLUDED_EXTS:
                continue
        filtered_items.append(entry)

    total = len(filtered_items)
    for i, entry in enumerate(filtered_items):
        es_ultimo = (i == total - 1)
        simbolo = "└── " if es_ultimo else "├── "
        linea = prefijo + simbolo + entry.name
        lineas.append(linea)
        if entry.is_dir(follow_symlinks=False):
            # No se recorre si el directorio termina en '.gdb' o es 'shp'
            if entry.name.lower().endswith(".gdb") or entry.name.lower() == "shp":
                continue
            if no_recursion:
                continue
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            lineas.extend(listar_contenido(entry.path, nuevo_prefijo, no_recursion=False))
    return lineas

def generar_arbol_principal(carpeta_madre: str) -> List[str]:
    """
    Genera el árbol principal de la estructura de carpetas.

    Args:
        carpeta_madre (str): Ruta de la carpeta madre.

    Returns:
        List[str]: Lista de líneas representando la estructura completa.
    """
    lineas: List[str] = []
    try:
        with os.scandir(carpeta_madre) as it:
            items = sorted([entry for entry in it if entry.is_dir()], key=lambda e: e.name.lower())
    except PermissionError:
        return ["[Sin permisos en la carpeta madre]"]

    for idx, entry in enumerate(items, start=1):
        lineas.append("")  # Salto de línea para separar secciones
        linea_principal = f"├── *{idx}. {entry.name}*"
        lineas.append(linea_principal)

        descripcion = ""
        for key, desc in DESCRIPTIONS.items():
            if key in entry.name.upper():
                descripcion = desc
                break
        if descripcion:
            lineas.append("")
            lineas.append("    Descripción: " + descripcion)
            lineas.append("")
        
        sub_path = entry.path
        if entry.name.upper() == "APRX":
            lineas.extend(listar_contenido(sub_path, "    ", no_recursion=True))
        else:
            lineas.extend(listar_contenido(sub_path, "    ", no_recursion=False))
    return lineas
