
from pathlib import Path
import pandas as pd


# =====================================================
# CONFIGURACION
# =====================================================

INPUT_FILE = Path("data/books.csv")
OUTPUT_FILE = Path("data/books_clean.csv")

REQUIRED_COLUMNS = [
    "title",
    "price_gbp",
    "availability",
    "rating",
    "product_url",
    "source_page"
]


# =====================================================
# 1. VALIDAR COLUMNAS
# =====================================================

def validate_columns(df):
    """Comprueba que el DataFrame tenga las columnas obligatorias."""

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Faltan columnas: {missing_columns}")


# =====================================================
# 2. LIMPIAR Y TRANSFORMAR DATOS
# =====================================================

def clean_data(df):
    """Limpia precios, calificaciones y disponibilidad."""

    validate_columns(df)

    df = df.copy()

    # Eliminar duplicados por URL
    df = df.drop_duplicates(
        subset=["product_url"],
        keep="first"
    ).copy()

    # Convertir precios a valores numericos
    price_text = df["price_gbp"].astype("string")

    price_extracted = price_text.str.extract(
        r"(\d+(?:\.\d+)?)",
        expand=False
    )

    df["price_gbp_numeric"] = pd.to_numeric(
        price_extracted,
        errors="coerce"
    )

    invalid_prices = (
        df["price_gbp_numeric"].isna()
        | (df["price_gbp_numeric"] <= 0)
    )

    df.loc[
        invalid_prices,
        "price_gbp_numeric"
    ] = float("nan")

    # Validar calificaciones
    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    invalid_ratings = (
        df["rating"].isna()
        | ~df["rating"].between(1, 5)
        | (df["rating"] % 1 != 0)
    )

    df.loc[
        invalid_ratings,
        "rating"
    ] = float("nan")

    # Identificar disponibilidad
    df["is_available"] = (
        df["availability"]
        .astype("string")
        .str.contains("In stock", case=False, na=False)
    )

    return df


# =====================================================
# 3. EJECUCION PRINCIPAL
# =====================================================

def main():

    print("\n===== PROCESAMIENTO Y CALIDAD DE DATOS =====")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"No se encontro: {INPUT_FILE}"
        )

    original_df = pd.read_csv(
        INPUT_FILE,
        encoding="utf-8"
    )

    initial_records = len(original_df)

    print(f"\nRegistros originales: {initial_records}")

    validate_columns(original_df)

    duplicates = original_df.duplicated(
        subset=["product_url"]
    ).sum()

    df = clean_data(original_df)

    print(f"Duplicados eliminados: {duplicates}")

    invalid_prices = df["price_gbp_numeric"].isna().sum()
    invalid_ratings = df["rating"].isna().sum()

    print(f"Precios invalidos: {invalid_prices}")
    print(f"Calificaciones invalidas: {invalid_ratings}")

    duplicate_titles = df["title"].duplicated().sum()

    print(f"\nTitulos repetidos: {duplicate_titles}")

    constant_columns = [
        col for col in df.columns
        if df[col].nunique(dropna=False) <= 1
    ]

    print("\nColumnas sin variabilidad:")

    if constant_columns:
        for col in constant_columns:
            print(f"- {col}")
    else:
        print("No se encontraron columnas constantes.")

    print("\n===== CALIDAD DE DATOS =====")
    print("\nValores faltantes por columna:")
    print(df.isnull().sum().to_string())

    print("\nRegistros finales:", len(df))

    # Guardar archivo limpio
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # Resumen estadistico
    print("\n===== RESUMEN ESTADISTICO =====")

    print("Total de libros:", len(df))

    print(
        "Precio promedio: GBP",
        round(df["price_gbp_numeric"].mean(), 2)
    )

    print(
        "Precio maximo: GBP",
        round(df["price_gbp_numeric"].max(), 2)
    )

    print(
        "Precio minimo: GBP",
        round(df["price_gbp_numeric"].min(), 2)
    )

    print(
        "Calificacion promedio:",
        round(df["rating"].mean(), 2)
    )

    print(
        "Libros disponibles:",
        int(df["is_available"].sum())
    )

    print(
        "Porcentaje disponible:",
        round(df["is_available"].mean() * 100, 2),
        "%"
    )

    print("\nArchivo generado:", OUTPUT_FILE)
    print("Proceso finalizado correctamente.")


if __name__ == "__main__":
    main()
