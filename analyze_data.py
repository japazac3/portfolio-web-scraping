
from pathlib import Path
import pandas as pd

# =====================================================
# CONFIGURACION
# =====================================================

INPUT_FILE = Path("data/books.csv")
OUTPUT_FILE = Path("data/books_clean.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# =====================================================
# 1. CARGAR DATOS
# =====================================================

print("\n===== PROCESAMIENTO Y CALIDAD DE DATOS =====")

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"No se encontro: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE, encoding="utf-8")

initial_records = len(df)

print(f"\nRegistros originales: {initial_records}")

# Verificar columnas obligatorias
required_columns = [
    "title",
    "price_gbp",
    "availability",
    "rating",
    "product_url",
    "source_page"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Faltan columnas: {missing_columns}")

# =====================================================
# 2. ELIMINAR DUPLICADOS POR URL
# =====================================================

duplicates = df.duplicated(subset=["product_url"]).sum()

df = df.drop_duplicates(
    subset=["product_url"],
    keep="first"
).copy()

print(f"Duplicados eliminados: {duplicates}")

# =====================================================
# 3. LIMPIAR Y CONVERTIR PRECIOS
# =====================================================

# Extraer el valor numerico aunque el simbolo de libra
# tenga problemas de codificacion.

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

df.loc[invalid_prices, "price_gbp_numeric"] = float("nan")

print(f"Precios invalidos: {invalid_prices.sum()}")

# =====================================================
# 4. VALIDAR CALIFICACIONES
# =====================================================

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

invalid_ratings = (
    df["rating"].isna()
    | ~df["rating"].between(1, 5)
    | (df["rating"] % 1 != 0)
)

df.loc[invalid_ratings, "rating"] = float("nan")

print(f"Calificaciones invalidas: {invalid_ratings.sum()}")

# =====================================================
# 5. IDENTIFICAR DISPONIBILIDAD
# =====================================================

df["is_available"] = (
    df["availability"]
    .astype("string")
    .str.contains("In stock", case=False, na=False)
)

# =====================================================
# 6. ANALISIS DE DUPLICADOS Y VARIABILIDAD
# =====================================================

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

# =====================================================
# 7. CALIDAD DE DATOS
# =====================================================

print("\n===== CALIDAD DE DATOS =====")

print("\nValores faltantes por columna:")
print(df.isnull().sum().to_string())

print("\nRegistros finales:", len(df))

# =====================================================
# 8. GUARDAR ARCHIVO LIMPIO
# =====================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# =====================================================
# 9. RESUMEN ESTADISTICO
# =====================================================

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
