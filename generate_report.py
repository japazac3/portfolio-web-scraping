
import pandas as pd
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

# Rutas
DATA_FILE = Path("data/books_clean.csv")
REPORT_DIR = Path("reports")
PDF_FILE = REPORT_DIR / "informe_analisis_libros.pdf"

REPORT_DIR.mkdir(exist_ok=True)

# Cargar datos
df = pd.read_csv(DATA_FILE)

# Indicadores
total = len(df)
precio_promedio = df["price_gbp_numeric"].mean()
precio_maximo = df["price_gbp_numeric"].max()
precio_minimo = df["price_gbp_numeric"].min()
calificacion_promedio = df["rating"].mean()
disponibles = df["is_available"].sum()

# Documento PDF
document = SimpleDocTemplate(
    str(PDF_FILE),
    pagesize=A4,
    rightMargin=1.8 * cm,
    leftMargin=1.8 * cm,
    topMargin=1.8 * cm,
    bottomMargin=1.8 * cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=20,
    leading=25,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Heading2"],
    textColor=colors.HexColor("#24527A"),
    spaceBefore=12,
    spaceAfter=8
)

story = []

# Portada
story.append(Paragraph(
    "INFORME DE ANÁLISIS DE DATOS",
    title_style
))

story.append(Paragraph(
    "Proyecto: Web Scraping y análisis de libros",
    styles["Heading2"]
))

story.append(Spacer(1, 12))

story.append(Paragraph(
    f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
    styles["Normal"]
))

story.append(Spacer(1, 20))

story.append(Paragraph(
    "1. INTRODUCCIÓN",
    subtitle_style
))

story.append(Paragraph(
    "Este proyecto utiliza Python para extraer, limpiar y analizar "
    "información de un catálogo de libros. Se emplearon Requests y "
    "BeautifulSoup para la extracción, Pandas para el procesamiento "
    "y Matplotlib/Seaborn para la visualización.",
    styles["BodyText"]
))

# Indicadores
story.append(Paragraph(
    "2. INDICADORES PRINCIPALES",
    subtitle_style
))

table_data = [
    ["Indicador", "Resultado"],
    ["Total de libros", f"{total:,}"],
    ["Precio promedio", f"£{precio_promedio:.2f}"],
    ["Precio máximo", f"£{precio_maximo:.2f}"],
    ["Precio mínimo", f"£{precio_minimo:.2f}"],
    ["Calificación promedio", f"{calificacion_promedio:.2f} / 5"],
    ["Libros disponibles", f"{disponibles:,}"]
]

table = Table(table_data, colWidths=[8 * cm, 7 * cm])

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 8),
    ("ALIGN", (1, 1), (1, -1), "CENTER")
]))

story.append(table)

# Gráficos
story.append(Paragraph(
    "3. VISUALIZACIÓN DE RESULTADOS",
    subtitle_style
))

charts = [
    ("01_distribucion_precios.png", "Distribución de precios"),
    ("02_calificaciones.png", "Calificaciones de los libros"),
    ("03_precio_por_calificacion.png", "Precio según calificación"),
    ("04_disponibilidad.png", "Disponibilidad de libros")
]

for filename, description in charts:
    image_path = REPORT_DIR / filename

    if image_path.exists():
        story.append(Paragraph(description, styles["Heading3"]))
        img = Image(str(image_path), width=15 * cm, height=8.5 * cm)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 12))

# Conclusiones
story.append(Paragraph(
    "4. CONCLUSIONES",
    subtitle_style
))

conclusions = [
    f"Se procesaron {total:,} registros de libros.",
    f"El precio promedio registrado fue de £{precio_promedio:.2f}.",
    f"La calificación promedio fue de {calificacion_promedio:.2f} sobre 5.",
    f"Se identificaron {disponibles:,} libros disponibles."
]

for conclusion in conclusions:
    story.append(Paragraph(
        f"• {conclusion}",
        styles["BodyText"]
    ))
    story.append(Spacer(1, 6))

# Generar PDF
document.build(story)

print("====================================")
print("INFORME GENERADO CORRECTAMENTE")
print("====================================")
print(f"Archivo: {PDF_FILE}")
