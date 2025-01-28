# ============================================================================
# === Metadata y Créditos ====================================================
# ============================================================================
# Realizado por: Jorge Vallejo @OnfeVS
# Fecha: 2024-01-28
# Descripción: Script para recortar una base de datos geográfica (GDB) utilizando un área de recorte definida por un shapefile.
# Créditos: Jorge Vallejo (@OnfeVS) - Autor principal
# Licencia: MIT
# ============================================================================

import arcpy
import os
import time

__author__ = "Jorge Vallejo @OnfeVS"
__version__ = "1.0.0"
__date__ = "2024-01-28"  # Fecha de última actualización

"""
Este script realiza el recorte de capas y datasets de una GDB utilizando un área de recorte definida por un shapefile.
"""

# ============================================================================
# === Configuraciones iniciales =================================================
# ============================================================================
arcpy.env.overwriteOutput = True

# ============================================================================
# === Funciones principales ==================================================
# ============================================================================

def get_all_datasets(gdb):
    """Obtiene todos los feature datasets recursivamente"""
    arcpy.env.workspace = gdb
    datasets = []
    for ds in arcpy.ListDatasets("", "Feature"):
        datasets.append(ds)
        sub_datasets = arcpy.ListDatasets(ds + "/*", "Feature")
        if sub_datasets:
            datasets.extend(sub_datasets)
    return datasets

def has_intersection(fc, clip_features):
    """Verifica si una capa tiene intersección con el área de recorte"""
    try:
        result = arcpy.SelectLayerByLocation_management(fc, "INTERSECT", clip_features, selection_type="NEW_SELECTION")
        count = int(arcpy.GetCount_management(result)[0])
        return count > 0
    except Exception as e:
        print(f"Error verificando intersección para {fc}: {e}")
        return False

def is_empty(fc):
    """Verifica si una capa está vacía"""
    try:
        count = int(arcpy.GetCount_management(fc)[0])
        return count == 0
    except Exception as e:
        print(f"Error verificando si la capa está vacía: {e}")
        return True

def get_unique_gdb_name(base_folder):
    """Genera un nombre único para la GDB de salida siguiendo el formato CartoBase_1, CartoBase_2, etc."""
    counter = 1
    while True:
        gdb_name = f"CartoBase_{counter}.gdb"
        gdb_path = os.path.join(base_folder, gdb_name)
        if not arcpy.Exists(gdb_path):
            return gdb_path
        counter += 1

def delete_unwanted_files(gdb_path):
    """Elimina archivos no deseados que se crean automáticamente en la GDB"""
    try:
        templates = ["GDB_EditingTemplates", "GDB_EditingTemplateRelationships"]
        for template in templates:
            template_path = os.path.join(gdb_path, template)
            if arcpy.Exists(template_path):
                arcpy.Delete_management(template_path)
                print(f"Archivo eliminado: {template_path}")
    except Exception as e:
        print(f"Error eliminando archivos no deseados: {e}")

def clip_layers(gdb_input, clip_features, gdb_output):
    """Procesa las capas y datasets recortando con un shapefile"""
    try:
        arcpy.env.workspace = gdb_input

        # Procesar capas en la raíz
        print("\nProcesando capas en la raíz...")
        for fc in arcpy.ListFeatureClasses():
            try:
                print(f"Verificando intersección para: {fc}...")
                if not has_intersection(fc, clip_features):
                    print(f"Sin intersección: {fc}. Omitiendo...")
                    continue

                output_fc = os.path.join(gdb_output, os.path.basename(fc))
                arcpy.Clip_analysis(fc, clip_features, output_fc)

                if is_empty(output_fc):
                    arcpy.Delete_management(output_fc)
                    print(f"Capa recortada vacía eliminada: {fc}")
                else:
                    print(f"Recortada: {fc}")
            except Exception as e:
                print(f"Error en capa raíz {fc}: {str(e)}")
                continue

        # Procesar datasets
        print("\nProcesando Feature Datasets...")
        all_datasets = get_all_datasets(gdb_input)

        if not all_datasets:
            print("¡No se encontraron datasets en la GDB de entrada!")
            return

        for fds in all_datasets:
            try:
                if not arcpy.Exists(os.path.join(gdb_input, fds)):
                    print(f"Dataset no existe en input: {fds}")
                    continue

                desc = arcpy.Describe(fds)
                output_fds = os.path.join(gdb_output, fds)

                # Crear dataset en la salida solo si tiene capas válidas
                dataset_has_data = False
                for fc in arcpy.ListFeatureClasses("", "", fds):
                    try:
                        print(f"Verificando intersección para: {fc}...")
                        if not has_intersection(fc, clip_features):
                            print(f"Sin intersección: {fc}. Omitiendo...")
                            continue

                        if not dataset_has_data:
                            arcpy.CreateFeatureDataset_management(gdb_output, fds, desc.spatialReference)
                            print(f"\nDataset creado: {fds}")
                            dataset_has_data = True

                        output_fc = os.path.join(gdb_output, fds, os.path.basename(fc))
                        arcpy.Clip_analysis(fc, clip_features, output_fc)

                        if is_empty(output_fc):
                            arcpy.Delete_management(output_fc)
                            print(f"Capa recortada vacía eliminada: {fds}/{os.path.basename(fc)}")
                        else:
                            print(f"Recortada: {fds}/{os.path.basename(fc)}")
                    except Exception as e:
                        print(f"Error en capa {fds}/{fc}: {str(e)}")
                        continue

                if not dataset_has_data:
                    print(f"Dataset vacío, no incluido: {fds}")
            except Exception as dataset_error:
                print(f"\nError crítico en dataset {fds}: {str(dataset_error)}")
                continue

        print("\n¡Proceso finalizado! Verifique los mensajes de advertencia.")

    except Exception as e:
        print(f"Error general: {str(e)}")

# ============================================================================
# === Función principal =======================================================
# ============================================================================
def main():
    """Función principal para ejecutar el script"""
    print("=== Script para Recortar GDB con un Área de Recorte ===")
    print(f"=== Versión: {__version__} | Autor: {__author__} ===")

    # Iniciar el cronómetro
    start_time = time.time()

    # Solicitar rutas al usuario
    gdb_input = input("Ingrese la ruta de la GDB de entrada: ").strip()
    clip_features = input("Ingrese la ruta del shapefile para el recorte: ").strip()
    output_folder = os.path.dirname(gdb_input)

    # Crear un nombre único para la GDB de salida
    gdb_output = get_unique_gdb_name(output_folder)

    # Crear la GDB de salida
    arcpy.CreateFileGDB_management(output_folder, os.path.basename(gdb_output))
    print(f"\nNueva GDB creada: {gdb_output}")

    # Validar rutas de entrada
    if all([arcpy.Exists(gdb_input), arcpy.Exists(clip_features)]):
        clip_layers(gdb_input, clip_features, gdb_output)
        delete_unwanted_files(gdb_output)
    else:
        print("Error: Verifique que las rutas de la GDB de entrada y el shapefile sean correctas.")

    # Finalizar el cronómetro y calcular tiempo
    elapsed_time = time.time() - start_time
    estimated_manual_time = 30 * 60  # 30 minutos en segundos
    time_saved_percentage = round(100 * (1 - (elapsed_time / estimated_manual_time)))

    print(f"\nTiempo total de ejecución: {elapsed_time:.2f} segundos.")


        # Mostrar créditos
    print("========================")
    print("\n=== Créditos ===")
    print(f"Realizado por: {__author__}")
    print("Contacto: @OnfeVS")
    print("========================")


    
    print(f"Acabas de ahorrarte un {time_saved_percentage}% de tiempo usando el script, "
          f"ya que esta tarea manual normalmente tomaría + de 30 minutos.")

# ============================================================================
# === Ejecución del script ====================================================
# ============================================================================
if __name__ == "__main__":
    main()
