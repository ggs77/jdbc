import csv
import os
import sys
import time
import logging
import json
from utils import load_config, DBManager

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CSVProcessor:
    """Clase para procesar la lectura y escritura de archivos CSV."""

    def __init__(self, config):
        self._config = config

    def read_ids(self):
        """Lee los IDs desde el archivo de entrada CSV."""
        try:
            input_path = os.path.join(self._config['paths']['input_dir'], self._config['files']['csv_input'])
            with open(input_path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # Saltar cabecera
                ids = [row[0] for row in reader]
            logging.info(f"Total de IDs cargados: {len(ids)}")
            return ids
        except FileNotFoundError:
            logging.error(f"Error: No se encontró el archivo '{input_path}'.")
            sys.exit(1)
        except IndexError:
            logging.error("Error: El archivo de entrada no contiene datos o la columna de IDs está vacía.")
            sys.exit(1)

    def write_results(self, results, headers, block_num, output_path):
        """Escribe los resultados en el archivo de salida CSV."""
        try:
            # Si el archivo no existe o es el primer bloque, escribir la cabecera
            if block_num == 1 and headers:
                mode = "w"  # Modo de escritura para el primer bloque
                with open(output_path, mode, newline="", encoding="utf-8") as f_out:
                    csv_writer = csv.writer(f_out)
                    csv_writer.writerow(headers)
                    csv_writer.writerows(results)
            else:
                mode = "a"  # Modo de añadir para los bloques siguientes
                with open(output_path, mode, newline="", encoding="utf-8") as f_out:
                    csv_writer = csv.writer(f_out)
                    csv_writer.writerows(results)
            logging.info(f"Bloque {block_num} procesado ({len(results)} filas)")
        except Exception as e:
            logging.error(f"❌ Error al escribir el bloque {block_num}: {e}")
            raise

def load_query(query_path):
    """Carga la consulta SQL desde un archivo."""
    try:
        with open(query_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"Error: No se encontró el archivo de consulta '{query_path}'.")
        sys.exit(1)

def main():
    """Función principal que orquesta el proceso."""
    
    # 1. Cargar configuración
    try:
        config = load_config('config/config.json')
    except (FileNotFoundError, json.JSONDecodeError):
        sys.exit(1)

    # Permitir pasar parámetros por línea de comandos, si no, usar la configuración
    try:
        block_size = int(sys.argv[1]) if len(sys.argv) > 1 else config['parameters']['block_size']
        pause = int(sys.argv[2]) if len(sys.argv) > 2 else config['parameters']['pause_seconds']
        query_file = sys.argv[3] if len(sys.argv) > 3 else config['files']['sql_query']
    except (ValueError, IndexError):
        logging.warning("Parámetros de línea de comandos inválidos. Usando valores por defecto de la configuración.")
        block_size = config['parameters']['block_size']
        pause = config['parameters']['pause_seconds']
        query_file = config['files']['sql_query']
        
    # Rutas de archivos
    query_path = os.path.join(config['paths']['queries_dir'], query_file)
    output_path = os.path.join(config['paths']['output_dir'], config['files']['csv_output'])

    # Inicializar procesador CSV y gestor de DB
    csv_processor = CSVProcessor(config)
    
    try:
        db_manager = DBManager(config)
        cursor = db_manager.get_cursor()
    except (ConnectionError, Exception):
        sys.exit(1)

    # 2. Leer IDs y consulta
    ids = csv_processor.read_ids()
    sql_template = load_query(query_path)

    # 3. Procesar en bloques
    total_ids = len(ids)
    if not ids:
        logging.info("No hay IDs para procesar. Finalizando.")
        sys.exit(0)

    for i in range(0, total_ids, block_size):
        block = ids[i:i + block_size]
        ids_str = ",".join(f"'{x}'" for x in block)
        sql_query = sql_template.replace("###IDS###", ids_str)
        
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
            
            csv_processor.write_results(results, headers, (i // block_size) + 1, output_path)

        except Exception as e:
            logging.error(f"❌ Error al ejecutar el bloque {(i // block_size) + 1}: {e}")
            break

        # 4. Pausa antes del siguiente bloque
        if i + block_size < total_ids:
            logging.info(f"⏸️ Pausando {pause} segundos...")
            time.sleep(pause)

    # 5. Cierre de recursos
    cursor.close()
    db_manager.close()
    logging.info(f"✅ Proceso finalizado. Resultados en {output_path}")

if __name__ == "__main__":
    main()