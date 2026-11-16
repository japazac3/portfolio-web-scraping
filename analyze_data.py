import pandas as pd

# Leer los datos extraídos
df = pd.read_csv("data/books.csv", encoding="utf-8")

# Eliminar registros duplicados
df = df.drop_duplicates(subset=["product_url"])

# Limpiar y convertir los precios
df["price_gbp_numeric"] = (
    df["price_gbp"]
    .astype(str)
    .str.replace("Â", "", regex=False)
    .str.replace("£", "", regex=False)
    .str.strip()
)

df["price_gbp_numeric"] = pd.to_numeric(
    df["price_gbp_numeric"],
    errors="coerce"
)

# Convertir calificaciones a valores numéricos
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Identificar disponibilidad
df["is_available"] = df["availability"].str.contains(
    "In stock",
    case=False,
    na=False
)

# Guardar archivo limpio
df.to_csv(
    "data/books_clean.csv",
    index=False,
    encoding="utf-8-sig"
)

# Mostrar resultados
print("\n===== RESUMEN DEL ANÁLISIS =====")
print("Total de libros:", len(df))
print("Precio promedio: £", round(df["price_gbp_numeric"].mean(), 2))
print("Precio máximo: £", round(df["price_gbp_numeric"].max(), 2))
print("Precio mínimo: £", round(df["price_gbp_numeric"].min(), 2))
print("Calificación promedio:", round(df["rating"].mean(), 2))
print("Libros disponibles:", df["is_available"].sum())

print("\nArchivo generado: data/books_clean.csv")
print("Proceso finalizado correctamente.")