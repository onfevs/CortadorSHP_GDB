import arcpy

# Configuración del entorno
arcpy.env.overwriteOutput = True

# Configuración general (puede extenderse o cargarse desde un archivo externo)
CONFIG = {
    "tiempo_estandar": 30 * 60,  # 30 minutos en segundos
}

