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
    filtered_items = [item for item in items if os.path.splitext(item)[1].lower() not in EXCLUDED_EXTS or os.path.isdir(os.path.join(ruta, item))]
    
    total = len(filtered_items)
    for i, item in enumerate(filtered_items):
        es_ultimo = (i == total - 1)
        simbolo = "└── " if es_ultimo else "├── "
        linea = prefijo + simbolo + item
        lineas.append(linea)
        full_path = os.path.join(ruta, item)
        if os.path.isdir(full_path) and not item.lower().endswith(".gdb") and item.lower() != "shp" and not no_recursion:
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            lineas.extend(listar_contenido(full_path, nuevo_prefijo, no_recursion=False))
    return lineas

def generar_arbol_principal(carpeta_madre):
    lineas = []
    items = [item for item in os.listdir(carpeta_madre) if os.path.isdir(os.path.join(carpeta_madre, item))]
    items.sort()
    
    for idx, item in enumerate(items, start=1):
        lineas.append("")
        linea_principal = "├── *{}. {}*".format(idx, item)
        lineas.append(linea_principal)
        
        descripcion = DESCRIPTIONS.get(item.upper().split('_')[0], "")
        if descripcion:
            lineas.append("")
            lineas.append("    Descripción: " + descripcion)
            lineas.append("")
        
        sub_path = os.path.join(carpeta_madre, item)
        lineas.extend(listar_contenido(sub_path, "    ", no_recursion=(item.upper() == "APRX")))
    return lineas

def analizar_campos(feature_class):
    """Devuelve dos listas: campos con datos y campos sin datos."""
    campos_con_datos = []
    campos_sin_datos = []
    try:
        campos = [f.name for f in arcpy.ListFields(feature_class) if f.type not in ["Geometry", "OID"]]
        for campo in campos:
            valores = [row[0] for row in arcpy.da.SearchCursor(feature_class, campo)]
            if all(v is None for v in valores):
                campos_sin_datos.append(campo)
            else:
                campos_con_datos.append(campo)
    except Exception as e:
        print(f"Error al analizar campos en {feature_class}: {e}")
    return campos_con_datos, campos_sin_datos

def listar_aclaraciones(carpeta_gdb):
    """Lista las aclaraciones sobre capas y tablas con campos sin información."""
    aclaraciones = []
    try:
        gdbs = [item for item in os.listdir(carpeta_gdb) if item.lower().endswith(".gdb")]
        for gdb in gdbs:
            gdb_path = os.path.join(carpeta_gdb, gdb)
            arcpy.env.workspace = gdb_path
            
            # Revisar Feature Datasets y sus capas
            datasets = arcpy.ListDatasets("", "Feature") or []
            for fds in datasets:
                arcpy.env.workspace = os.path.join(gdb_path, fds)
                fcs = arcpy.ListFeatureClasses() or []
                fc_info = []
                for fc in fcs:
                    campos_con_datos, campos_sin_datos = analizar_campos(fc)
                    if campos_sin_datos:  # Solo incluir si hay campos sin datos
                        fc_info.append((fc, campos_sin_datos))
                if fc_info:
                    aclaraciones.append((gdb, fds, "FeatureClass", fc_info))
            
            # Revisar tablas independientes
            arcpy.env.workspace = gdb_path
            tablas = arcpy.ListTables() or []
            tabla_info = []
            for tabla in tablas:
                campos_con_datos, campos_sin_datos = analizar_campos(tabla)
                if campos_sin_datos:  # Solo incluir si hay campos sin datos
                    tabla_info.append((tabla, campos_sin_datos))
            if tabla_info:
                aclaraciones.append((gdb, "Tablas", "Table", tabla_info))
    except Exception as e:
        print(f"Error al listar aclaraciones: {e}")
    return aclaraciones

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
        f.write(f"Proyecto: {nombre_proyecto}\n")
        f.write(f"Operador: {operador}\n\n")
        f.write("Estructura de carpetas y archivos:\n")
        
        # Generar la estructura principal
        arbol = generar_arbol_principal(carpeta_madre)
        for linea in arbol:
            f.write(linea + "\n")
        
        # Agregar sección de aclaraciones
        f.write("\n1. ACLARACIONES\n")
        carpeta_gdb = os.path.join(carpeta_madre, "GDB")
        if os.path.exists(carpeta_gdb):
            aclaraciones = listar_aclaraciones(carpeta_gdb)
            if aclaraciones:
                for idx_fds, (gdb, fds, tipo, items) in enumerate(aclaraciones, start=1):
                    f.write(f"\n\t1.{idx_fds} {fds} en la GDB {gdb}\n")
                    for idx_item, (item, campos_sin_datos) in enumerate(items, start=1):
                        justificacion = "No se presenta datos debido a que no se cuenta con esta información para el diligenciamiento en la GDB."
                        # Ejemplo de justificación alternativa basada en nombres específicos
                        if any(x in item for x in ["UsosyUsuariosRecursoHidrico", "Vertimiento", "Captacion"]):
                            justificacion = "No presentan datos debido a que no aplican para el proyecto minero."
                        
                        f.write(f"\t\t1.{idx_fds}.{idx_item} {tipo} {item}\n")
                        if campos_sin_datos:
                            f.write(f"\t\t\t- Campos sin datos: {', '.join(campos_sin_datos)}\n")
                        f.write(f"\t\t\t- Justificación: {justificacion}\n")
            else:
                f.write("\tNo se encontraron capas o tablas con campos sin datos.\n")
        else:
            f.write("\tLa carpeta 'GDB' no existe en la ruta especificada.\n")

    print(f"Estructura generada correctamente en '{archivo_salida}'.")

if __name__ == "__main__":
    main()


