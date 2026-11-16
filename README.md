# Python Web Scraping & Data Analysis

## Descripción del proyecto

Proyecto de extracción, limpieza, análisis y visualización de datos desarrollado con Python.

El sistema obtiene información de un catálogo de libros mediante Web Scraping, procesa los registros con Pandas, genera gráficos estadísticos y produce un informe automático en PDF.

## Tecnologías utilizadas

- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- Seaborn
- ReportLab

## Funcionalidades

1. Extracción automática de información de libros.
2. Navegación por páginas del catálogo.
3. Limpieza y transformación de datos.
4. Eliminación de registros duplicados.
5. Análisis de precios y calificaciones.
6. Generación de cuatro gráficos estadísticos.
7. Creación automática de informes PDF.

## Estructura

```text
portfolio_web_scraping/
├── data/
├── reports/
├── tests/
├── scraper.py
├── analyze_data.py
├── visualize_data.py
├── generate_report.py
├── requirements.txt
└── README.md
```

## Instalación

```bash
python -m venv .venv
```

Activar entorno virtual en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python scraper.py
python analyze_data.py
python visualize_data.py
python generate_report.py
```

## Resultados

Los archivos generados se almacenan en:

- `data/`: datos originales y procesados.
- `reports/`: gráficos e informe PDF.

## Objetivo profesional

Demostrar conocimientos prácticos de Python, automatización, extracción de información, procesamiento de datos y generación de reportes.

## Fuente de datos

Proyecto educativo: [Books to Scrape](https://books.toscrape.com/).

La extracción se realiza con fines de aprendizaje y respetando las condiciones del sitio.

## Autor

Portafolio de desarrollo Python y análisis de datos.

## 📊 Resultados y visualizaciones

El proyecto genera cuatro gráficos estadísticos para facilitar la interpretación de los datos extraídos.

### 1. Distribución de precios

![Distribución de precios](reports/01_distribucion_precios.png)

### 2. Calificaciones de libros

![Calificaciones](reports/02_calificaciones.png)

### 3. Precio promedio según calificación

![Precio por calificación](reports/03_precio_por_calificacion.png)

### 4. Disponibilidad de libros

![Disponibilidad](reports/04_disponibilidad.png)

## 📄 Informe automático en PDF

El sistema genera un informe con indicadores estadísticos, gráficos y conclusiones.

[Consultar informe de análisis de libros](reports/informe_analisis_libros.pdf)