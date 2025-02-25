import os
import arcpy
from typing import List
from logging_utils import logging_print

def get_all_datasets(gdb: str) -> List[str]:
    """
    Obtiene todos los feature datasets recursivamente de la GDB.
    
    Args:
        gdb (str): Ruta de la geodatabase.
        
    Returns:
        List[str]: Lista de nombres de datasets.
    """
    arcpy.env.workspace = gdb
    datasets: List[str] = []
    for ds in arcpy.ListDatasets("", "Feature") or []:
        datasets.append(ds)
        sub_datasets = arcpy.ListDatasets(ds + "/*", "Feature")
        if sub_datasets:
            datasets.extend(sub_datasets)
    return datasets

def has_intersection(fc: str, clip_features: str) -> bool:
    """
    Verifica si una capa tiene intersección con el área de recorte.
    
    Args:
        fc (str): Ruta o nombre de la capa.
        clip_features (str): Ruta del shapefile de recorte.
        
    Returns:
        bool: True si existe intersección; de lo contrario, False.
    """
    try:
        resultado = arcpy.SelectLayerByLocation_management(fc, "INTERSECT", clip_features, selection_type="NEW_SELECTION")
        count = int(arcpy.GetCount_management(resultado)[0])
        return count > 0
    except arcpy.ExecuteError as e:
        logging_print(f"Error verificando intersección para {fc}: {e}", nivel="error")
        return False

def is_empty(fc: str) -> bool:
    """
    Verifica si una capa está vacía.
    
    Args:
        fc (str): Ruta o nombre de la capa.
        
    Returns:
        bool: True si la capa está vacía; de lo contrario, False.
    """
    try:
        count = int(arcpy.GetCount_management(fc)[0])
        return count == 0
    except arcpy.ExecuteError as e:
        logging_print(f"Error verificando si la capa está vacía: {e}", nivel="error")
        return True

def clip_layers(gdb_input: str, clip_features: str, gdb_output: str) -> None:
    """
    Procesa las capas y datasets recortando con un shapefile.
    
    Args:
        gdb_input (str): Ruta de la GDB de entrada.
        clip_features (str): Ruta del shapefile para recorte.
        gdb_output (str): Ruta de la GDB de salida.
    """
    try:
        arcpy.env.workspace = gdb_input

        # Procesar capas en la raíz
        logging_print("Procesando capas en la raíz...")
        for fc in arcpy.ListFeatureClasses() or []:
            try:
                logging_print(f"Verificando intersección para: {fc}...")
                if not has_intersection(fc, clip_features):
                    logging_print(f"Sin intersección: {fc}. Omitiendo...")
                    continue

                output_fc = os.path.join(gdb_output, os.path.basename(fc))
                arcpy.Clip_analysis(fc, clip_features, output_fc)

                if is_empty(output_fc):
                    arcpy.Delete_management(output_fc)
                    logging_print(f"Capa recortada vacía eliminada: {fc}")
                else:
                    logging_print(f"Recortada: {fc}")
            except arcpy.ExecuteError as e:
                logging_print(f"Error en capa raíz {fc}: {e}", nivel="error")
                continue

        # Procesar datasets
        logging_print("Procesando Feature Datasets...")
        all_datasets = get_all_datasets(gdb_input)

        if not all_datasets:
            logging_print("¡No se encontraron datasets en la GDB de entrada!")
            return

        for fds in all_datasets:
            try:
                if not arcpy.Exists(os.path.join(gdb_input, fds)):
                    logging_print(f"Dataset no existe en input: {fds}", nivel="warning")
                    continue

                desc = arcpy.Describe(fds)
                dataset_has_data = False

                for fc in arcpy.ListFeatureClasses("", "", fds) or []:
                    try:
                        logging_print(f"Verificando intersección para: {fc}...")
                        if not has_intersection(fc, clip_features):
                            logging_print(f"Sin intersección: {fc}. Omitiendo...")
                            continue

                        if not dataset_has_data:
                            arcpy.CreateFeatureDataset_management(gdb_output, fds, desc.spatialReference)
                            logging_print(f"Dataset creado: {fds}")
                            dataset_has_data = True

                        output_fc = os.path.join(gdb_output, fds, os.path.basename(fc))
                        arcpy.Clip_analysis(fc, clip_features, output_fc)

                        if is_empty(output_fc):
                            arcpy.Delete_management(output_fc)
                            logging_print(f"Capa recortada vacía eliminada: {fds}/{os.path.basename(fc)}")
                        else:
                            logging_print(f"Recortada: {fds}/{os.path.basename(fc)}")
                    except arcpy.ExecuteError as e:
                        logging_print(f"Error en capa {fds}/{fc}: {e}", nivel="error")
                        continue

                if not dataset_has_data:
                    logging_print(f"Dataset vacío, no incluido: {fds}", nivel="warning")
            except arcpy.ExecuteError as e:
                logging_print(f"Error crítico en dataset {fds}: {e}", nivel="error")
                continue

        # Procesar tablas en la raíz
        logging_print("Procesando tablas en la raíz...")
        for tabla in arcpy.ListTables() or []:
            if tabla.endswith("TB"):
                if not is_empty(tabla):
                    arcpy.Copy_management(tabla, os.path.join(gdb_output, os.path.basename(tabla)))
                    logging_print(f"Copiada: {tabla}")
                else:
                    logging_print(f"Tabla vacía, no copiada: {tabla}", nivel="warning")
            else:
                logging_print(f"Tabla no procesada (no termina en TB): {tabla}")
                
        logging_print("¡Proceso finalizado! Verifique los mensajes de advertencia.")
    except arcpy.ExecuteError as e:
        logging_print(f"Error general: {e}", nivel="error")


