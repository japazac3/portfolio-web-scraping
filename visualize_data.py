
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =====================================================
# CONFIGURACION GENERAL
# =====================================================

DATA_FILE = Path("data/books_clean.csv")
REPORT_DIR = Path("reports")

REQUIRED_COLUMNS = [
    "title",
    "rating",
    "price_gbp_numeric",
    "is_available"
]

CHART_FILES = [
    "01_distribucion_precios.png",
    "02_calificaciones.png",
    "03_precio_por_calificacion.png",
    "04_disponibilidad.png",
    "05_libros_mas_caros.png",
    "06_libros_mas_economicos.png"
]


# =====================================================
# VALIDACION Y PREPARACION
# =====================================================

def prepare_data(df):
    """Valida y prepara los datos para generar los graficos."""

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Faltan columnas requeridas: {missing_columns}"
        )

    df = df.copy()

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

    if df.empty:
        raise ValueError(
            "No existen registros validos para generar graficos."
        )

    return df


# =====================================================
# GENERACION DE VISUALIZACIONES
# =====================================================

def generate_charts(df, report_dir=REPORT_DIR):
    """Genera seis graficos y devuelve sus rutas."""

    df = prepare_data(df)

    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(
        style="whitegrid",
        palette="deep",
        font_scale=1.1
    )

    total_books = len(df)
    average_price = df["price_gbp_numeric"].mean()
    median_price = df["price_gbp_numeric"].median()

    print("\n===== GENERACION DE VISUALIZACIONES =====")
    print(f"Libros analizados: {total_books}")
    print(f"Precio promedio: GBP {average_price:.2f}")
    print(f"Precio mediano: GBP {median_price:.2f}")

    generated_files = []

    # -------------------------------------------------
    # 1. DISTRIBUCION DE PRECIOS
    # -------------------------------------------------

    fig, ax = plt.subplots(figsize=(11, 6))

    sns.histplot(
        data=df,
        x="price_gbp_numeric",
        bins=30,
        kde=True,
        ax=ax
    )

    ax.axvline(
        average_price,
        linestyle="--",
        linewidth=2,
        label=f"Promedio: GBP {average_price:.2f}"
    )

    ax.axvline(
        median_price,
        linestyle=":",
        linewidth=2,
        label=f"Mediana: GBP {median_price:.2f}"
    )

    ax.set_title(
        "Distribucion de precios de libros",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Precio (GBP)")
    ax.set_ylabel("Cantidad de libros")
    ax.legend()

    fig.tight_layout()

    output = report_dir / CHART_FILES[0]
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_files.append(output)

    # -------------------------------------------------
    # 2. DISTRIBUCION DE CALIFICACIONES
    # -------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.countplot(
        data=df,
        x="rating",
        order=sorted(df["rating"].dropna().unique()),
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, padding=3)

    ax.set_title(
        "Cantidad de libros por calificacion",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Calificacion (1 a 5 estrellas)")
    ax.set_ylabel("Cantidad de libros")

    fig.tight_layout()

    output = report_dir / CHART_FILES[1]
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_files.append(output)

    # -------------------------------------------------
    # 3. PRECIO PROMEDIO POR CALIFICACION
    # -------------------------------------------------

    rating_prices = (
        df.groupby("rating")["price_gbp_numeric"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.barplot(
        data=rating_prices,
        x="rating",
        y="price_gbp_numeric",
        errorbar=None,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.2f",
            padding=3
        )

    ax.set_title(
        "Precio promedio segun calificacion",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Calificacion")
    ax.set_ylabel("Precio promedio (GBP)")

    fig.tight_layout()

    output = report_dir / CHART_FILES[2]
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_files.append(output)

    # -------------------------------------------------
    # 4. DISPONIBILIDAD DE LIBROS
    # -------------------------------------------------

    availability = (
        df["is_available"]
        .astype(str)
        .str.lower()
        .map({
            "true": "Disponible",
            "false": "No disponible"
        })
        .value_counts()
        .reindex(
            ["Disponible", "No disponible"],
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x=availability.index,
        y=availability.values,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, padding=3)

    ax.set_title(
        "Disponibilidad de libros",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Estado")
    ax.set_ylabel("Cantidad de libros")

    fig.tight_layout()

    output = report_dir / CHART_FILES[3]
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_files.append(output)

    # -------------------------------------------------
    # 5. DIEZ LIBROS MAS CAROS
    # -------------------------------------------------

    most_expensive = (
        df.nlargest(10, "price_gbp_numeric")
        .sort_values("price_gbp_numeric")
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    sns.barplot(
        data=most_expensive,
        x="price_gbp_numeric",
        y="title",
        ax=ax
    )

    ax.set_title(
        "Los 10 libros mas caros",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Precio (GBP)")
    ax.set_ylabel("Titulo del libro")

    fig.tight_layout()

    output = report_dir / CHART_FILES[4]
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_files.append(output)

    # -------------------------------------------------
    # 6. DIEZ LIBROS MAS ECONOMICOS
    # -------------------------------------------------

    cheapest = (
        df.nsmallest(10, "price_gbp_numeric")
        .sort_values(
            "price_gbp_numeric",
            ascending=False
        )
    )

    fig, ax = plt.subplots(figsize=(14, 9))

    sns.barplot(
        data=cheapest,
        x="price_gbp_numeric",
        y="title",
        ax=ax
    )

    ax.set_title(
        "Los 10 libros mas economicos",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Precio (GBP)")
    ax.set_ylabel("Titulo del libro")

    fig.subplots_adjust(
        left=0.48,
        right=0.97,
        top=0.91,
        bottom=0.10
    )

    output = report_dir / CHART_FILES[5]
    fig.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.25
    )
    plt.close(fig)
    generated_files.append(output)

    # -------------------------------------------------
    # RESUMEN FINAL
    # -------------------------------------------------

    print("\n======================================")
    print("ANALISIS GRAFICO COMPLETADO")
    print("======================================")

    print("Total de libros analizados:", total_books)
    print("Graficos generados:", len(generated_files))

    for file in generated_files:
        print("-", file.name)

    print("\nProceso finalizado correctamente.")

    return generated_files


# =====================================================
# EJECUCION PRINCIPAL
# =====================================================

def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    generate_charts(df, REPORT_DIR)


if __name__ == "__main__":
    main()
