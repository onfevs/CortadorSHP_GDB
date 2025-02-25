import configparser
import logging
from pathlib import Path
from typing import Optional

class Configuracion:
    """Clase para manejar la configuración del script desde un archivo externo."""
    
    def __init__(self, config_path: str = None):
        # Determinar la ruta del archivo config.ini relativa al directorio del script
        if config_path is None:
            base_dir = Path(__file__).resolve().parent.parent  # Sube un nivel desde src/ a project/
            config_path = base_dir / "config" / "config.ini"
        
        self.config = configparser.ConfigParser()
        
        # Verificar si el archivo existe
        if not config_path.exists():
            logging.basicConfig(level=logging.INFO)  # Configuración básica por defecto
            logging.warning(f"No se encontró config.ini en {config_path}. Usando valores por defecto.")
            self._cargar_config_por_defecto()
        else:
            self.config.read(config_path)
            if not self.config.sections():
                logging.warning(f"config.ini en {config_path} está vacío o mal formado. Usando valores por defecto.")
                self._cargar_config_por_defecto()
            else:
                self.setup_logging()

    def _cargar_config_por_defecto(self) -> None:
        """Carga valores por defecto si el archivo de configuración no está disponible."""
        self.config['Paths'] = {'output_base': 'C:/GIS Projects'}
        self.config['Settings'] = {
            'log_level': 'INFO',
            'estimated_manual_time': '1800',
            'gdb_prefix': 'CartoBase'
        }
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configura el logging según el nivel especificado en el config."""
        nivel = self.config["Settings"].get("log_level", "INFO")
        logging.basicConfig(
            level=getattr(logging, nivel),
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def obtener_ruta_base(self) -> Path:
        """Obtiene la ruta base para la salida desde el config."""
        return Path(self.config["Paths"]["output_base"])

    def obtener_prefijo_gdb(self) -> str:
        """Obtiene el prefijo para nombres de GDB."""
        return self.config["Settings"]["gdb_prefix"]

    def obtener_tiempo_manual(self) -> int:
        """Obtiene el tiempo manual estimado en segundos."""
        try:
            return self.config["Settings"].getint("estimated_manual_time")
        except ValueError as e:
            logging.warning(f"Valor inválido para estimated_manual_time: {e}. Usando 1800 como predeterminado.")
            return 1800  # Valor por defecto si la conversión falla
