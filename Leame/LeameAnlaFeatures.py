import os
import arcpy

# Lista de extensiones de archivos a excluir (en minúsculas)
EXCLUDED_EXTS = [".gdb", ".xlsx", ".jpg", ".cfe", ".cfs", ".si", ".gen"]

# Diccionario con descripciones SEO-friendly para carpetas principales
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
            if item.lower().endswith(".gdb"):
                continue
            if item.lower() == "shp":
                continue
            if no_recursion:
                continue
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            lineas.extend(listar_contenido(full_path, nuevo_prefijo, no_recursion=False))
    return lineas

def generar_arbol_principal(carpeta_madre):
    lineas = []
    items = [item for item in os.listdir(carpeta_madre) if os.path.isdir(os.path.join(carpeta_madre, item))]
    items.sort()
    
    for idx, item in enumerate(items, start=1):
        lineas.append("")  # Salto de línea para separar secciones
        linea_principal = "├── *{}. {}*".format(idx, item)
        lineas.append(linea_principal)
        
        descripcion = ""
        for key, desc in DESCRIPTIONS.items():
            if key in item.upper():
                descripcion = desc
                break
        if descripcion:
            lineas.append("")
            lineas.append("    Descripción: " + descripcion)
            lineas.append("")
        
        sub_path = os.path.join(carpeta_madre, item)
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

    # Identificar la carpeta GDB y procesar Feature Classes sin información
    gdb_folder = os.path.join(carpeta_madre, "GDB")
    feature_classes_sin_informacion = {}

    if os.path.exists(gdb_folder):
        gdbs = [os.path.join(gdb_folder, item) for item in os.listdir(gdb_folder) 
                if item.lower().endswith(".gdb") and os.path.isdir(os.path.join(gdb_folder, item))]
        for gdb in gdbs:
            try:
                arcpy.env.workspace = gdb
                # Feature Classes en la raíz
                fcs_root = arcpy.ListFeatureClasses() or []
                empty_fcs_root = []
                for fc in fcs_root:
                    if arcpy.GetCount_management(fc).getOutput(0) == '0':
                        alias_name = arcpy.Describe(fc).aliasName or fc
                        empty_fcs_root.append((fc, alias_name))
                
                # Feature Datasets
                datasets = arcpy.ListDatasets(feature_type='Feature') or []
                empty_datasets = {}
                for dataset in datasets:
                    fcs = arcpy.ListFeatureClasses(feature_dataset=dataset) or []
                    empty_fcs = []
                    for fc in fcs:
                        if arcpy.GetCount_management(fc).getOutput(0) == '0':
                            alias_name = arcpy.Describe(fc).aliasName or fc
                            empty_fcs.append((fc, alias_name))
                    if empty_fcs:
                        empty_datasets[dataset] = empty_fcs
                
                if empty_fcs_root or empty_datasets:
                    feature_classes_sin_informacion[gdb] = {'root': empty_fcs_root, 'datasets': empty_datasets}
            except Exception as e:
                print(f"Error al acceder a la GDB {gdb}: {e}")
                continue

    # Generar el archivo de salida
    archivo_salida = "informe_estructura_proyecto.txt"
    with open(archivo_salida, "w", encoding="utf-8") as f:
        # Encabezado del informe
        f.write("Proyecto: {}\n".format(nombre_proyecto))
        f.write("Operador: {}\n\n".format(operador))
        f.write("Estructura de carpetas y archivos:\n")
        
        # Estructura de carpetas
        arbol = generar_arbol_principal(carpeta_madre)
        for linea in arbol:
            f.write(linea + "\n")
        
        # Sección de aclaraciones
        f.write("\n. ACLARACIONES\n")
        if feature_classes_sin_informacion:
            f.write("---------------LISTA DE LOS FEATURE CLASSES SIN INFORMACIÓN---------------------\n")
            for gdb, info in feature_classes_sin_informacion.items():
                f.write(f"GDB: {os.path.basename(gdb)}\n")
                if info['root']:
                    f.write("  Feature Classes en la raíz:\n")
                    f.write("    {:<30} {:<50} {:<30}\n".format('FEATURE CLASS', 'ALIAS NAME', "NOTA"))
                    for fc_name, alias_name in info['root']:
                        f.write("    {:<30} {:<50} {:<30}\n".format(fc_name, alias_name, "No aplica para este proyecto"))
                for dataset, fcs in info['datasets'].items():
                    f.write(f"  Feature Dataset: {dataset}\n")
                    f.write("    {:<30} {:<50} {:<30}\n".format('FEATURE CLASS', 'ALIAS NAME', "NOTA"))
                    for fc_name, alias_name in fcs:
                        f.write("    {:<30} {:<50} {:<30}\n".format(fc_name, alias_name, "No aplica para este proyecto"))
        else:
            f.write("No se encontraron Feature Classes sin información en las GDBs.\n")

    print("Estructura generada correctamente en '{}'.".format(archivo_salida))

if __name__ == "__main__":
    main()


