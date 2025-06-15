Analizador-lite
Herramienta open-source para análisis descriptivo y diagnóstico de datos en archivos CSV, con exportación automática de resultados a PDF.
Descripción del Proyecto
Esta herramienta Lite fue desarrollada como una versión simplificada pero funcional de un sistema multiagente complejo.
Su objetivo es ofrecer análisis rápidos, claros y reutilizables sobre datasets en formato CSV, con enfoque en calidad de datos, trazabilidad y facilidad de uso.
El proyecto surge como parte de un proceso de aprendizaje autodidacta enfocado en análisis de datos y DevOps.
No sigue un temario formal, pero integra buenas prácticas desde su concepción.
Ha sido desplegado en servidor propio y optimizado para uso individual, con posibilidad de evolucionar hacia una solución colaborativa o en modelo SaaS.

Características principales
- Validación estructural y de calidad de datos
- Limpieza automatizada de valores nulos, duplicados y errores comunes
- Estadísticas descriptivas y detección de valores atípicos
- Exportación de informe PDF con resultados clave
- Registro automático de cada análisis en base de datos SQLite
- Acceso seguro mediante PIN vía Streamlit
- Arquitectura modular, documentada y extensible

Enfoque Lite y Decisiones de Diseño
- Se han eliminado los módulos avanzados (machine learning, generación de insights, recomendación o prescripción) por su complejidad y coste computacional.
- Se mantiene un flujo mínimo pero completo: validación, limpieza, análisis y exportación en PDF.
- Todo el código está diseñado para ser trazable, estable y fácilmente mantenible.
- Se emplean librerías comunes y código documentado para facilitar la comprensión y posible colaboración.

Estructura del Proyecto
├── README.md
├── agentes/ # Módulos de validación, limpieza, análisis y generación de PDF
│ ├── analizador_descriptivo.py
│ ├── generador_pdf.py
│ ├── limpiador_datos.py
│ └── validador_dataset.py
├── app/ # App principal en Streamlit y orquestador
│ ├── app.py
│ └── orquestador.py
├── core/ # Sistema de logging y persistencia en base de datos
│ ├── persistencia.py
│ └── sistema_logging.py
├── fonts/ # Fuente para informes PDF
│ └── LiberationSans-Regular.ttf
├── scripts/ # Scripts de arranque y configuración
│ ├── launch_streamlit.sh
│ └── setup_lite.sh
├── tests/ # Tests unitarios básicos
│ └── test_validador.py
├── data/ # Entrada, salida, históricos y base de datos
├── requirements.txt
└── LICENSE MIT

Flujo de Ejecución
1. El usuario accede a la aplicación a través de Streamlit (`app/app.py`).
2. Se autentica mediante un PIN local definido en el código.
3. Sube un archivo CSV de entrada.
4. El sistema valida la estructura, limpia los datos y realiza el análisis.
5. Los resultados se muestran en pantalla y pueden exportarse a PDF.
6. Se registra automáticamente el análisis en base de datos.

Dependencias
- Python 3.12+
- streamlit
- pandas
- matplotlib
- fpdf
- sqlite3 (módulo estándar de Python)

Datos y Archivos
•	Entrada activa: data/entrada/activa.csv
•	Histórico de archivos: data/entrada/historico/
•	Salida limpia: data/salida/datos_limpios.csv
•	Resumen de análisis: data/salida/resultados/resumen_analisis.csv
•	Informe PDF: data/salida/resultados/informe_lite.pdf

Autenticación y Seguridad
•	Acceso mediante PIN configurable en app.py.
•	No se almacenan contraseñas ni datos personales del usuario.

Base de Datos
•	SQLite local en data/db/asistente_datos.db.
•	Cada análisis se registra con nombre de archivo, fecha, tamaño y resumen.

Testing y Validación
•	Pruebas mínimas en el módulo /tests.
•	Validación funcional del flujo con datasets reales.
•	Revisión completa de procesos y módulos multiagente asistida por ChatGPT.

Despliegue
•	Aplicación desplegada como servicio systemd en servidor Linux.
•	Acceso externo configurado mediante proxy NGINX.

Caso de uso realista
Ejemplo: análisis de ventas mensuales en una pyme (archivo ventas_abril.csv)
1.	El usuario accede a la app desde el navegador y se autentica.
2.	Sube el archivo CSV. Este se almacena como activa.csv y se guarda una copia en el histórico.
3.	Se ejecuta el análisis automáticamente: validación, limpieza y resumen descriptivo.
4.	Se muestran estadísticas clave en pantalla: número de registros, medias, valores únicos, etc.
5.	Se genera el informe PDF y se pone a disposición para descarga directa.
6.	El análisis queda registrado en la base de datos y puede ser consultado posteriormente.
Este flujo permite a cualquier usuario obtener un diagnóstico rápido y claro de sus datos sin conocimientos técnicos.

Posibles tareas futuras y/o módulos pendientes
•	Mejora del sistema de logs con buscador y filtros
•	Inclusión de transformaciones previas al análisis
•	Soporte para múltiples archivos y análisis comparativo
•	Visualización de resultados directamente en la interfaz Streamlit
•	Desarrollo de versión multiusuario o basada en la nube (SaaS)


Instalación
```bash
pip install -r requirements.txt





