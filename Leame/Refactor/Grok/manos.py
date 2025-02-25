import os
from typing import List
from corazon import DESCRIPTIONS
from ojos import listar_contenido

def generar_arbol_principal(carpeta_madre: str) -> List[str]:
    """
    Genera el árbol principal de carpetas con descripciones SEO-friendly.

    Args:
        carpeta_madre (str): Ruta de la carpeta raíz.

    Returns:
        List[str]: Lista de líneas del árbol generado.
    """
    lineas: List[str] = []
    try:
        items = sorted([
            item for item in os.listdir(carpeta_madre)
            if os.path.isdir(os.path.join(carpeta_madre, item))
        ])
    except OSError as e:
        return [f"Error al acceder a {carpeta_madre}: {str(e)}"]

    for idx, item in enumerate(items, start=1):
        lineas.append("")  # Salto de línea
        lineas.append(f"├── *{idx}. {item}*")

        # Buscar descripción
        descripcion = next(
            (desc for key, desc in DESCRIPTIONS.items() if key in item.upper()),
            ""
        )
        if descripcion:
            lineas.extend(["", f"    Descripción: {descripcion}", ""])

        sub_path = os.path.join(carpeta_madre, item)
        no_recursion = item.upper() == "APRX"
        lineas.extend(listar_contenido(sub_path, "    ", no_recursion))

    return lineas