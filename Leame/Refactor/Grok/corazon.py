from typing import Dict, List

# Configuración externa (podría moverse a un archivo JSON/YAML)
EXCLUDED_EXTS: List[str] = [".gdb", ".xlsx", ".jpg", ".cfe", ".cfs", ".si", ".gen"]

DESCRIPTIONS: Dict[str, str] = {
    "GDB": "Contiene bases de datos geográficas esenciales con información espacial crítica del proyecto minero.",
    "PDF": "Almacena planos en formato PDF que permiten la visualización detallada de los mapas del proyecto minero.",
    "MXD": "Incluye archivos MXD que facilitan la edición y visualización precisa de la cartografía del proyecto.",
    "APRX": "Contiene archivos APRX editados en ArcGIS Pro, permitiendo análisis avanzado y modificaciones geoespaciales.",
    "METADATOS": "Almacena metadatos en formato XML, proporcionando información estructurada y detallada del proyecto minero.",
    "RASTER": "Contiene imágenes ortofotográficas en formato TIFF que muestran el área del título minero en alta resolución.",
    "CSV": "Incluye archivos CSV con coordenadas y datos críticos de monitoreo, muestreo y puntos estratégicos del proyecto."
}