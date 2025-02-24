import os

# Lista de extensiones de archivos a excluir (en minúsculas)
EXCLUDED_EXTS = [".gdb", ".xlsx", ".jpg", ".cfe", ".cfs", ".si", ".gen"]

# Diccionario con descripciones SEO-friendly para carpetas principales.
DESCRIPTIONS = {
    "GDB": "Contiene bases de datos geográficas esenciales con información espacial crítica del proyecto minero.",
    "PDF": "Almacena planos en formato PDF que permiten la visualización detallada de los mapas del proyecto minero.",
    "MXD": "Incluye archivos MXD que facilitan la edición y visualización precisa de la cartografía del proyecto.",
    "APRX": "Contiene archivos APRX editados en ArcGIS Pro, permitiendo análisis avanzado y modificaciones geoespaciales.",
    "METADATOS": "Almacena metadatos en formato XML, proporcionando información estructurada y detallada del proyecto minero.",
    "RASTER": "Contiene imágenes ortofotográficas en formato TIFF que muestran el área del título minero en alta resolución.",
    "CSV": "Incluye archivos CSV con coordenadas y datos críticos de monitoreo, muestreo y puntos estratégicos del proyecto."
}

def listar_contenido(ruta, prefijo, no_recursion=False):
    lineas = []
    try:
        items = os.listdir(ruta)
    except PermissionError:
        return [prefijo + "└── [Sin permisos]"]
    
    items.sort()
    # Filtrar archivos por extensión
    filtered_items = []
    for item in items:
        full_path = os.path.join(ruta, item)
        if os.path.isfile(full_path):
            ext = os.path.splitext(item)[1].lower()
            if ext in EXCLUDED_EXTS:
                continue
        filtered_items.append(item)
    
    total = len(filtered_items)
    for i, item in enumerate(filtered_items):
        es_ultimo = (i == total - 1)
        simbolo = "└── " if es_ultimo else "├── "
        linea = prefijo + simbolo + item
        lineas.append(linea)
        full_path = os.path.join(ruta, item)
        if os.path.isdir(full_path):
            # Si el directorio termina en '.gdb', no se recorre.
            if item.lower().endswith(".gdb"):
                continue
            # Si es la carpeta "shp", se lista pero no se recorre su contenido.
            if item.lower() == "shp":
                continue
            # Si no se requiere recursión, no se desciende.
            if no_recursion:
                continue
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            lineas.extend(listar_contenido(full_path, nuevo_prefijo, no_recursion=False))
    return lineas

def generar_arbol_principal(carpeta_madre):
    lineas = []
    # Se obtienen solo las carpetas directas en la carpeta madre.
    items = [item for item in os.listdir(carpeta_madre) if os.path.isdir(os.path.join(carpeta_madre, item))]
    items.sort()
    
    for idx, item in enumerate(items, start=1):
        lineas.append("")  # Salto de línea para separar secciones
        # Línea de carpeta principal en negrita y numerada
        linea_principal = "├── *{}. {}*".format(idx, item)
        lineas.append(linea_principal)
        
        # Buscar la descripción comparando mayúsculas
        descripcion = ""
        for key, desc in DESCRIPTIONS.items():
            if key in item.upper():
                descripcion = desc
                break
        if descripcion:
            lineas.append("")  # Salto de línea entre la carpeta y la descripción
            lineas.append("    Descripción: " + descripcion)
            lineas.append("")  # Salto de línea entre la descripción y el contenido
        
        sub_path = os.path.join(carpeta_madre, item)
        # Si la carpeta es APRX, solo se listan sus archivos inmediatos sin recursión.
        if item.upper() == "APRX":
            lineas.extend(listar_contenido(sub_path, "    ", no_recursion=True))
        else:
            lineas.extend(listar_contenido(sub_path, "    ", no_recursion=False))
    return lineas

def main():
    # Solicita los datos del proyecto
    nombre_proyecto = input("Ingrese el Nombre del Proyecto: ")
    operador = input("Ingrese el Operador: ")
    carpeta_madre = input("Ingrese la ruta de la Carpeta Madre (con todas las subcarpetas): ")

    if not os.path.isdir(carpeta_madre):
        print("La ruta especificada no es una carpeta válida.")
        return

    archivo_salida = "informe_estructura_proyecto.txt"
    with open(archivo_salida, "w", encoding="utf-8") as f:
        # Encabezado del informe
        f.write("Proyecto: {}\n".format(nombre_proyecto))
        f.write("Operador: {}\n\n".format(operador))
        f.write("Estructura de carpetas y archivos:\n")
        
        # Genera la estructura y la escribe en el archivo
        arbol = generar_arbol_principal(carpeta_madre)
        for linea in arbol:
            f.write(linea + "\n")
    
    print("Estructura generada correctamente en '{}'.".format(archivo_salida))

if __name__ == "__main__":
    main()


