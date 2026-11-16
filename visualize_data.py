
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuración
Path("reports").mkdir(exist_ok=True)

# Cargar datos limpios
df = pd.read_csv("data/books_clean.csv")

# Configuración visual
sns.set_theme(style="whitegrid")

# 1. Distribución de precios
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df,
    x="price_gbp_numeric",
    bins=30,
    kde=True
)
plt.title("Distribución de precios de libros")
plt.xlabel("Precio (£)")
plt.ylabel("Cantidad de libros")
plt.tight_layout()
plt.savefig("reports/01_distribucion_precios.png")
plt.close()

# 2. Cantidad de libros por calificación
plt.figure(figsize=(9, 5))
sns.countplot(
    data=df,
    x="rating",
    order=sorted(df["rating"].dropna().unique())
)
plt.title("Cantidad de libros por calificación")
plt.xlabel("Calificación")
plt.ylabel("Cantidad de libros")
plt.tight_layout()
plt.savefig("reports/02_calificaciones.png")
plt.close()

# 3. Precio promedio por calificación
plt.figure(figsize=(9, 5))
sns.barplot(
    data=df,
    x="rating",
    y="price_gbp_numeric",
    errorbar=None
)
plt.title("Precio promedio según calificación")
plt.xlabel("Calificación")
plt.ylabel("Precio promedio (£)")
plt.tight_layout()
plt.savefig("reports/03_precio_por_calificacion.png")
plt.close()

# 4. Disponibilidad de libros
availability = df["is_available"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    availability,
    labels=["Disponible" if x else "No disponible"
            for x in availability.index],
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Disponibilidad de libros")
plt.tight_layout()
plt.savefig("reports/04_disponibilidad.png")
plt.close()

print("================================")
print("ANÁLISIS GRÁFICO COMPLETADO")
print("================================")
print("Se generaron 4 gráficos en la carpeta reports/")
