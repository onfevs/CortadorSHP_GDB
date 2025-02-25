import logging
from typing import Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def log_info(mensaje: str) -> None:
    """Registra un mensaje de nivel INFO."""
    logger.info(mensaje)

def log_error(mensaje: str) -> None:
    """Registra un mensaje de nivel ERROR."""
    logger.error(mensaje)

def obtener_entrada_usuario(prompt: str) -> Optional[str]:
    """
    Solicita entrada al usuario y valida que no esté vacía.

    Args:
        prompt (str): Mensaje a mostrar al usuario.

    Returns:
        Optional[str]: Entrada válida o None si hay error.
    """
    try:
        entrada = input(prompt).strip()
        if not entrada:
            raise ValueError("La entrada no puede estar vacía.")
        return entrada
    except EOFError:
        log_error("Error de entrada/salida al leer datos del usuario.")
        return None