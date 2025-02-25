import logging
from typing import Any

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def logging_print(mensaje: str, nivel: str = "info") -> None:
    """
    Imprime el mensaje con el nivel de log especificado.
    
    Args:
        mensaje (str): Mensaje a imprimir.
        nivel (str, opcional): Nivel de log ('info', 'warning', 'error', etc.). Por defecto es 'info'.
    """
    nivel = nivel.lower()
    if nivel == "info":
        logging.info(mensaje)
    elif nivel == "warning":
        logging.warning(mensaje)
    elif nivel == "error":
        logging.error(mensaje)
    else:
        logging.debug(mensaje)


