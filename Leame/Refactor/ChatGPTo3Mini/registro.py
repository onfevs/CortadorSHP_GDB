"""
Módulo de registro que reemplaza el uso de print para mostrar mensajes.
"""

import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def loggingprint(message: Any) -> None:
    """
    Registra un mensaje de información.
    
    Args:
        message (Any): Mensaje a registrar.
    """
    logging.info(message)
