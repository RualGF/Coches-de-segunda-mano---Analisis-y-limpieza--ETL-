import pandas as pd

# Leemos el archivo limpio con pandas
df_limpio = pd.read_csv("coches_segunda_mano_limpio.csv")
df_limpio.describe()

# Contamos la cantidad de coches matriculados por año y los ordenamos de mayor a menor
porcentaje_coches_por_anyo = (df_limpio['year'].value_counts(normalize=True) * 100).round(2).astype(str) + ' %'
porcentaje_coches_por_anyo.rename("Mayor cantidad de coches matriculados por año en porcentaje")

# Contamos la cantidad de coches con potencia mayor a la media y los expresamos en porcentaje
media = df_limpio["potencia_cv"].mean()
porcentaje_potencia = (df_limpio[df_limpio['potencia_cv'] > media]['potencia_cv'].value_counts(normalize=True) * 100).round(2).astype(str) + ' %'
porcentaje_potencia.rename("Cantidad de coches con potencia mayor a la media en porcentaje")

# Mostramos las tres categorías que menos se repiten en la columna tipo_combustible
df_limpio['tipo_combustible'].value_counts().sort_values(ascending=True).rename(
    "Las tres categorías que menos se repiten en tipo de combustible").head(3)

# Mostramos el distintivo ambiental que tiene el coche con mayor precio
df_limpio.groupby("distintivo_ambiental").agg({"precio": "mean"}).sort_values(by="precio", ascending=False).head(1)

# Mostramos el año con menor emisión media de CO2
df_limpio.groupby("year").agg({"co2": "mean"}).sort_values(by="co2", ascending=True).head(1)