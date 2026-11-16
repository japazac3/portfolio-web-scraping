
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
    PageBreak,
    KeepTogether
)

# =====================================================
# 1. CONFIGURACION
# =====================================================

DATA_FILE = Path("data/books_clean.csv")
REPORT_DIR = Path("reports")
PDF_FILE = REPORT_DIR / "informe_analisis_libros.pdf"

REPORT_DIR.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"No se encontro: {DATA_FILE}")

# =====================================================
# 2. CARGA Y VALIDACION DE DATOS
# =====================================================

df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")

required_columns = [
    "title",
    "rating",
    "price_gbp_numeric",
    "is_available"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Faltan columnas necesarias: {missing_columns}"
    )

df["price_gbp_numeric"] = pd.to_numeric(
    df["price_gbp_numeric"], errors="coerce"
)

df["rating"] = pd.to_numeric(
    df["rating"], errors="coerce"
)

df["is_available"] = (
    df["is_available"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["true", "1", "yes", "si", "sí"])
)

valid_prices = df["price_gbp_numeric"].dropna()
valid_ratings = df["rating"].dropna()

if valid_prices.empty:
    raise ValueError("No existen precios numericos validos.")

if valid_ratings.empty:
    raise ValueError("No existen calificaciones validas.")

total = len(df)
total_precios = len(valid_prices)
total_calificaciones = len(valid_ratings)

precio_promedio = valid_prices.mean()
precio_mediano = valid_prices.median()
precio_maximo = valid_prices.max()
precio_minimo = valid_prices.min()
desviacion_precio = valid_prices.std()

calificacion_promedio = valid_ratings.mean()

disponibles = int(df["is_available"].sum())
no_disponibles = total - disponibles

porcentaje_disponible = (
    disponibles / total * 100 if total else 0
)

fecha_generacion = datetime.now().strftime(
    "%d/%m/%Y %H:%M"
)

# =====================================================
# 3. ESTILOS DEL DOCUMENTO
# =====================================================

document = SimpleDocTemplate(
    str(PDF_FILE),
    pagesize=A4,
    rightMargin=1.8 * cm,
    leftMargin=1.8 * cm,
    topMargin=2.0 * cm,
    bottomMargin=2.0 * cm,
    title="Informe de Analisis de Libros",
    author="Proyecto de Python - Web Scraping",
    subject="Extraccion, limpieza y analisis de datos"
)

styles = getSampleStyleSheet()

navy = colors.HexColor("#17365D")
blue = colors.HexColor("#24527A")
light_blue = colors.HexColor("#EAF1F8")
gray = colors.HexColor("#555555")

cover_title = ParagraphStyle(
    "CoverTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=25,
    leading=32,
    textColor=navy,
    alignment=1,
    spaceAfter=20
)

cover_subtitle = ParagraphStyle(
    "CoverSubtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=20,
    textColor=blue,
    alignment=1
)

section_style = ParagraphStyle(
    "SectionTitle",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=18,
    textColor=navy,
    spaceBefore=14,
    spaceAfter=10
)

chart_title = ParagraphStyle(
    "ChartTitle",
    parent=styles["Heading3"],
    fontSize=11,
    leading=15,
    textColor=blue,
    spaceBefore=8,
    spaceAfter=5
)

body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=15,
    textColor=gray,
    alignment=4,
    spaceAfter=8
)

small_style = ParagraphStyle(
    "SmallText",
    parent=styles["Normal"],
    fontSize=9,
    leading=13,
    textColor=gray
)

# =====================================================
# 4. ENCABEZADO Y PIE DE PAGINA
# =====================================================

def add_page_number(canvas, doc):
    canvas.saveState()

    width, height = A4

    canvas.setStrokeColor(colors.HexColor("#D9E2F0"))
    canvas.line(
        1.8 * cm,
        1.5 * cm,
        width - 1.8 * cm,
        1.5 * cm
    )

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(gray)

    canvas.drawString(
        1.8 * cm,
        1.1 * cm,
        "Proyecto de Web Scraping y Analisis de Datos"
    )

    canvas.drawRightString(
        width - 1.8 * cm,
        1.1 * cm,
        f"Pagina {doc.page}"
    )

    canvas.restoreState()


# =====================================================
# 5. CONSTRUCCION DEL INFORME
# =====================================================

story = []

# PORTADA

story.append(Spacer(1, 3.0 * cm))

story.append(Paragraph(
    "INFORME DE<br/>ANALISIS DE DATOS",
    cover_title
))

story.append(Paragraph(
    "PROYECTO DE WEB SCRAPING CON PYTHON",
    cover_subtitle
))

story.append(Spacer(1, 1.2 * cm))

story.append(Paragraph(
    "Extraccion, limpieza, procesamiento y "
    "visualizacion de datos de un catalogo de libros.",
    cover_subtitle
))

story.append(Spacer(1, 2.0 * cm))

cover_data = [
    ["INFORMACION DEL PROYECTO", "DETALLE"],
    ["Lenguaje", "Python 3"],
    ["Extraccion", "Requests y BeautifulSoup"],
    ["Procesamiento", "Pandas"],
    ["Visualizacion", "Matplotlib y Seaborn"],
    ["Generacion del informe", "ReportLab"],
    ["Registros analizados", f"{total:,}"],
    ["Fecha", fecha_generacion]
]

cover_table = Table(
    cover_data,
    colWidths=[6 * cm, 9 * cm]
)

cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), navy),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("BACKGROUND", (0, 1), (-1, -1), light_blue),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 9),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
]))

story.append(cover_table)

story.append(Spacer(1, 2.0 * cm))

story.append(Paragraph(
    "Documento generado automaticamente mediante Python.",
    small_style
))

story.append(PageBreak())

# RESUMEN EJECUTIVO

story.append(Paragraph(
    "1. RESUMEN EJECUTIVO",
    section_style
))

story.append(Paragraph(
    f"El presente proyecto tiene como objetivo demostrar "
    f"un proceso completo de extraccion y analisis de datos "
    f"utilizando Python. Se recopilaron y procesaron "
    f"{total:,} registros de un catalogo de libros, "
    f"permitiendo estudiar sus precios, calificaciones "
    f"y disponibilidad.",
    body_style
))

story.append(Paragraph(
    f"El precio promedio fue de £{precio_promedio:.2f}, "
    f"mientras que la calificacion promedio alcanzo "
    f"{calificacion_promedio:.2f} sobre 5. "
    f"Se identificaron {disponibles:,} libros disponibles.",
    body_style
))

# INDICADORES

story.append(Paragraph(
    "2. INDICADORES PRINCIPALES",
    section_style
))

table_data = [
    ["Indicador", "Resultado"],
    ["Total de registros", f"{total:,}"],
    ["Precios validos", f"{total_precios:,}"],
    ["Precio promedio", f"£{precio_promedio:.2f}"],
    ["Precio mediano", f"£{precio_mediano:.2f}"],
    ["Precio minimo", f"£{precio_minimo:.2f}"],
    ["Precio maximo", f"£{precio_maximo:.2f}"],
    ["Desviacion estandar", f"£{desviacion_precio:.2f}"],
    ["Calificacion promedio", f"{calificacion_promedio:.2f} / 5"],
    ["Libros disponibles", f"{disponibles:,}"],
    ["Libros no disponibles", f"{no_disponibles:,}"],
    ["Disponibilidad", f"{porcentaje_disponible:.1f}%"]
]

indicators_table = Table(
    table_data,
    colWidths=[8 * cm, 7 * cm],
    repeatRows=1
)

indicators_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), navy),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.white, light_blue]),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D3DF")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 7),
    ("ALIGN", (1, 1), (1, -1), "CENTER")
]))

story.append(indicators_table)

# METODOLOGIA

story.append(Paragraph(
    "3. METODOLOGIA",
    section_style
))

methodology = [
    "<b>Extraccion:</b> Requests y BeautifulSoup para "
    "obtener informacion del catalogo de libros.",
    "<b>Limpieza:</b> Pandas para validar, transformar "
    "y preparar los registros.",
    "<b>Analisis:</b> Calculo de estadisticas descriptivas "
    "sobre precios y calificaciones.",
    "<b>Visualizacion:</b> Matplotlib y Seaborn para "
    "representar los resultados mediante graficos.",
    "<b>Reporte:</b> ReportLab para generar automaticamente "
    "el documento PDF."
]

for item in methodology:
    story.append(Paragraph(
        f"- {item}",
        body_style
    ))

# ANALISIS VISUAL

story.append(Paragraph(
    "4. VISUALIZACION DE RESULTADOS",
    section_style
))

charts = [
    (
        "01_distribucion_precios.png",
        "4.1 Distribucion de precios",
        "Representa la frecuencia de los precios registrados."
    ),
    (
        "02_calificaciones.png",
        "4.2 Calificaciones de los libros",
        "Muestra la cantidad de libros por nivel de calificacion."
    ),
    (
        "03_precio_por_calificacion.png",
        "4.3 Precio promedio por calificacion",
        "Permite comparar el precio promedio segun la valoracion."
    ),
    (
        "04_disponibilidad.png",
        "4.4 Disponibilidad de libros",
        "Presenta la distribucion de los libros disponibles."
    ),
    (
        "05_libros_mas_caros.png",
        "4.5 Libros con precios mas elevados",
        "Identifica los diez libros de mayor precio."
    ),
    (
        "06_libros_mas_economicos.png",
        "4.6 Libros con precios mas bajos",
        "Identifica los diez libros de menor precio."
    )
]

for filename, heading, description in charts:

    image_path = REPORT_DIR / filename

    if image_path.exists():

        chart_image = Image(str(image_path))

        max_width = 16 * cm
        max_height = 9 * cm

        scale = min(
            max_width / chart_image.imageWidth,
            max_height / chart_image.imageHeight
        )

        chart_image.drawWidth = chart_image.imageWidth * scale
        chart_image.drawHeight = chart_image.imageHeight * scale
        chart_image.hAlign = "CENTER"

        story.append(KeepTogether([
            Paragraph(heading, chart_title),
            Paragraph(description, small_style),
            Spacer(1, 5),
            chart_image,
            Spacer(1, 12)
        ]))

    else:
        story.append(Paragraph(
            f"Grafico no encontrado: {filename}",
            small_style
        ))

# CONCLUSIONES

story.append(Paragraph(
    "5. CONCLUSIONES",
    section_style
))

conclusions = [
    f"Se analizaron {total:,} registros del catalogo de libros.",

    f"El precio promedio fue de £{precio_promedio:.2f}, "
    f"con un valor minimo de £{precio_minimo:.2f} "
    f"y un maximo de £{precio_maximo:.2f}.",

    f"La calificacion promedio fue de "
    f"{calificacion_promedio:.2f} sobre 5.",

    f"Se encontraron {disponibles:,} libros disponibles, "
    f"equivalentes al {porcentaje_disponible:.1f}% "
    f"del total."
]

if no_disponibles == 0:
    conclusions.append(
        "Todos los registros figuran como disponibles. "
        "Por tanto, este conjunto de datos no permite "
        "comparar categorias de disponibilidad."
    )

if total != df["title"].nunique():
    conclusions.append(
        "Existen titulos repetidos en el catalogo; "
        "esto no implica necesariamente registros "
        "duplicados por URL."
    )

for conclusion in conclusions:
    story.append(Paragraph(
        f"- {conclusion}",
        body_style
    ))

# CIERRE

story.append(Spacer(1, 15))

story.append(Paragraph(
    "FIN DEL INFORME",
    ParagraphStyle(
        "Closing",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=navy,
        alignment=1
    )
))

# =====================================================
# 6. GENERAR PDF
# =====================================================

document.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
)

print("=" * 50)
print("INFORME GENERADO CORRECTAMENTE")
print("=" * 50)
print(f"Archivo: {PDF_FILE}")
print(f"Registros analizados: {total:,}")
print(f"Precio promedio: £{precio_promedio:.2f}")
print(f"Calificacion promedio: {calificacion_promedio:.2f}/5")
print(f"Disponibilidad: {porcentaje_disponible:.1f}%")
print("=" * 50)
