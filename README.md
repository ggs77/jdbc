# 📦 Procesador de Datos Genérico con JDBC

Herramienta de Python para extraer datos de cualquier base de datos compatible con JDBC, procesarlos en bloques y guardarlos en un archivo CSV. El script ha sido optimizado para ser reusable, configurable y fácil de mantener.

## 📋 Requisitos

Asegúrate de tener los siguientes requisitos instalados en tu sistema:

- Python 3.6+
- Driver JDBC para tu base de datos (por ejemplo, `jt400.jar` para AS400, `postgresql.jar` para PostgreSQL).
- Java Runtime Environment (JRE) para ejecutar el driver JDBC.

Puedes instalar las dependencias de Python con el siguiente comando:

```
pip install -r requirements.txt
```

## 🚀 Uso

1. **Clonar el repositorio:**

   ```
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. **Configurar:**

   - Modifica el archivo de configuración `config/config.json` con los detalles de tu base de datos, rutas de archivos y parámetros de ejecución. Asegúrate de que los valores de `url`, `driver_class` y `driver_path` coincidan con tu base de datos y driver específico.
   - Coloca tu archivo CSV de entrada (con los IDs en la primera columna) en la carpeta `data/input/`. Asegúrate de que su nombre coincida con el valor de `csv_input` en el archivo de configuración.
   - Personaliza o añade tus consultas SQL en la carpeta `queries/`.

3. **Ejecutar el script:**

   ```
   python src/main.py [BLOCK_SIZE] [PAUSE_SECONDS] [QUERY_FILE]
   ```

   - `[BLOCK_SIZE]` (opcional): Número de IDs a procesar por bloque. Si no se especifica, se usará el valor de `config.json`.
   - `[PAUSE_SECONDS]` (opcional): Segundos de pausa entre cada bloque. Si no se especifica, se usará el valor de `config.json`.
   - `[QUERY_FILE]` (opcional): Nombre del archivo de consulta SQL (ej. `query.sql`). Si no se especifica, se usará el valor de `config.json`.

   **Ejemplo:**

   ```
   python src/main.py 50 2 my_query.sql
   ```

## 📁 Estructura del Proyecto

```
.
├── config/                  # Archivos de configuración
│   └── config.json          # Configuración principal (DB, rutas, etc.)
├── data/                    # Archivos de datos
│   ├── input/               # Archivos de entrada (ej. entrada.csv)
│   └── output/              # Archivos de salida (ej. salida.csv)
├── queries/                 # Archivos de consultas SQL (puedes tener múltiples)
│   ├── query.sql            # Consulta SQL reusable
│   └── another_query.sql    # Otra consulta de ejemplo
├── src/                     # Código fuente principal
│   ├── main.py              # Lógica principal del script
│   └── utils.py             # Funciones y clases de utilidad (DBManager, etc.)
├── .gitignore               # Archivos y carpetas a ignorar por Git
├── README.md                # Documentación del proyecto
└── requirements.txt         # Dependencias de Python
```

## 📖 Notas de Diseño

- **Separación de Responsabilidades:** El código está dividido en módulos (`main.py`, `utils.py`) y clases (`DBManager`, `CSVProcessor`) con responsabilidades claras y únicas.
- **Flexibilidad Genérica:** El script está diseñado para funcionar con cualquier base de datos JDBC, permitiendo cambiar fácilmente la configuración y el driver sin modificar el código.
- **Configuración Externa:** Los valores sensibles y de configuración están en `config.json` para facilitar su gestión y evitar modificar el código.
- **Consultas Reusables:** La lógica SQL se separa en archivos en la carpeta `queries`, permitiendo cambiar la consulta fácilmente mediante un parámetro.
- **Patrón Singleton:** La clase `DBManager` utiliza este patrón para asegurar que solo exista una conexión a la base de datos a la vez, optimizando recursos.
- **Documentación:** El código y la estructura del proyecto están documentados con comentarios y un `README.md` detallado.

## 🤝 Contribuciones

Si encuentras un error o tienes una mejora, no dudes en abrir un *issue* o enviar un *pull request*.