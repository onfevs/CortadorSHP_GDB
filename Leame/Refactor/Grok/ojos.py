import os
from typing import List
from corazon import EXCLUDED_EXTS

def listar_contenido(ruta: str, prefijo: str, no_recursion: bool = False) -> List[str]:
    """
    Lista el contenido de una carpeta excluyendo extensiones específicas y aplicando reglas de recursión.

    Args:
        ruta (str): Ruta de la carpeta a listar.
        prefijo (str): Prefijo para la representación visual del árbol.
        no_recursion (bool): Si True, no realiza recursión en subcarpetas.

    Returns:
        List[str]: Lista de líneas representando la estructura.
    """
    lineas: List[str] = []
    try:
        items = sorted(os.listdir(ruta))
    except PermissionError:
        return [f"{prefijo}└── [Sin permisos]"]
    except OSError as e:
        return [f"{prefijo}└── [Error: {str(e)}]"]

    filtered_items = [
        item for item in items
        if os.path.isdir(os.path.join(ruta, item)) or os.path.splitext(item)[1].lower() not in EXCLUDED_EXTS
    ]

    for i, item in enumerate(filtered_items):
        es_ultimo = (i == len(filtered_items) - 1)
        simbolo = "└── " if es_ultimo else "├── "
        linea = f"{prefijo}{simbolo}{item}"
        lineas.append(linea)

        full_path = os.path.join(ruta, item)
        if os.path.isdir(full_path) and not no_recursion:
            if item.lower().endswith(".gdb") or item.lower() == "shp":
                continue
            nuevo_prefijo = f"{prefijo}{'    ' if es_ultimo else '│   '}"
            lineas.extend(listar_contenido(full_path, nuevo_prefijo))

    return lineas