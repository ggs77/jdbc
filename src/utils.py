import jaydebeapi
import json
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path):
    """Carga la configuración desde un archivo JSON."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Error: El archivo de configuración '{config_path}' no fue encontrado.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error: El archivo de configuración '{config_path}' no es un JSON válido.")
        raise

class DBManager:
    """
    Clase para gestionar la conexión y operaciones con la base de datos.
    Implementa el patrón de diseño Singleton para la conexión.
    """
    _instance = None
    
    def __new__(cls, config):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance._conn = None
            cls._instance._config = config
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Establece la conexión con la base de datos."""
        try:
            db_conf = self._config['database']
            self._conn = jaydebeapi.connect(
                db_conf['driver_class'],
                db_conf['url'],
                [db_conf['user'], db_conf['password']],
                db_conf['driver_path']
            )
            logging.info("✅ Conexión a la base de datos establecida.")
        except Exception as e:
            logging.error(f"❌ Error al conectar a la base de datos: {e}")
            self._conn = None  # Resetear la conexión fallida
            raise

    def get_cursor(self):
        """Devuelve un objeto cursor para ejecutar consultas."""
        if self._conn:
            return self._conn.cursor()
        else:
            raise ConnectionError("No hay una conexión activa con la base de datos.")

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self._conn:
            self._conn.close()
            logging.info("✅ Conexión a la base de datos cerrada.")
            self._conn = None
            DBManager._instance = None  # Resetear la instancia para futuras conexiones

    def __del__(self):
        """Garantiza que la conexión se cierre al destruir el objeto."""
        self.close()