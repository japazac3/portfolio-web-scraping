
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# CONFIGURACION GENERAL
# =====================================================

DATA_FILE = Path("data/books_clean.csv")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(
    style="whitegrid",
    palette="deep",
    font_scale=1.1
)

# Cargar datos
if not DATA_FILE.exists():
    raise FileNotFoundError(f"No existe {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

# Validar columnas
required_columns = [
    "title",
    "rating",
    "price_gbp_numeric",
    "is_available"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Falta la columna: {column}")

df["price_gbp_numeric"] = pd.to_numeric(
    df["price_gbp_numeric"],
    errors="coerce"
)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df = df.dropna(
    subset=["price_gbp_numeric", "rating"]
).copy()

# Indicadores generales
total_books = len(df)
average_price = df["price_gbp_numeric"].mean()
median_price = df["price_gbp_numeric"].median()

print("\n===== GENERACION DE VISUALIZACIONES =====")
print(f"Libros analizados: {total_books}")
print(f"Precio promedio: GBP {average_price:.2f}")
print(f"Precio mediano: GBP {median_price:.2f}")


# =====================================================
# 1. DISTRIBUCION DE PRECIOS
# =====================================================

plt.figure(figsize=(11, 6))

sns.histplot(
    data=df,
    x="price_gbp_numeric",
    bins=30,
    kde=True
)

plt.axvline(
    average_price,
    linestyle="--",
    linewidth=2,
    label=f"Promedio: GBP {average_price:.2f}"
)

plt.axvline(
    median_price,
    linestyle=":",
    linewidth=2,
    label=f"Mediana: GBP {median_price:.2f}"
)

plt.title(
    "Distribucion de precios de libros",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Precio (GBP)")
plt.ylabel("Cantidad de libros")
plt.legend()

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "01_distribucion_precios.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 2. DISTRIBUCION DE CALIFICACIONES
# =====================================================

plt.figure(figsize=(9, 5))

ax = sns.countplot(
    data=df,
    x="rating",
    order=sorted(df["rating"].dropna().unique())
)

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title(
    "Cantidad de libros por calificacion",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Calificacion (1 a 5 estrellas)")
plt.ylabel("Cantidad de libros")

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "02_calificaciones.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 3. PRECIO PROMEDIO POR CALIFICACION
# =====================================================

rating_prices = (
    df.groupby("rating")["price_gbp_numeric"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(9, 5))

ax = sns.barplot(
    data=rating_prices,
    x="rating",
    y="price_gbp_numeric",
    errorbar=None
)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.2f",
        padding=3
    )

plt.title(
    "Precio promedio segun calificacion",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Calificacion")
plt.ylabel("Precio promedio (GBP)")

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "03_precio_por_calificacion.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 4. DISPONIBILIDAD DE LIBROS
# =====================================================

availability = (
    df["is_available"]
    .astype(str)
    .str.lower()
    .map({"true": "Disponible", "false": "No disponible"})
    .value_counts()
    .reindex(["Disponible", "No disponible"], fill_value=0)
)

plt.figure(figsize=(8, 5))

ax = sns.barplot(
    x=availability.index,
    y=availability.values
)

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title(
    "Disponibilidad de libros",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Estado")
plt.ylabel("Cantidad de libros")

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "04_disponibilidad.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 5. DIEZ LIBROS MAS CAROS
# =====================================================

most_expensive = (
    df.nlargest(10, "price_gbp_numeric")
    .sort_values("price_gbp_numeric")
)

plt.figure(figsize=(11, 7))

sns.barplot(
    data=most_expensive,
    x="price_gbp_numeric",
    y="title"
)

plt.title(
    "Los 10 libros mas caros",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Precio (GBP)")
plt.ylabel("Titulo del libro")

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "05_libros_mas_caros.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# 6. DIEZ LIBROS MAS ECONOMICOS
# =====================================================

cheapest = (
    df.nsmallest(10, "price_gbp_numeric")
    .sort_values("price_gbp_numeric", ascending=False)
)

plt.figure(figsize=(11, 7))

sns.barplot(
    data=cheapest,
    x="price_gbp_numeric",
    y="title"
)

plt.title(
    "Los 10 libros mas economicos",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Precio (GBP)")
plt.ylabel("Titulo del libro")

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "06_libros_mas_economicos.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =====================================================
# RESUMEN FINAL
# =====================================================

print("\n======================================")
print("ANALISIS GRAFICO COMPLETADO")
print("======================================")

print("Total de libros analizados:", total_books)
print("Graficos generados: 6")

for file in sorted(REPORT_DIR.glob("*.png")):
    print("-", file.name)

print("\nProceso finalizado correctamente.")
