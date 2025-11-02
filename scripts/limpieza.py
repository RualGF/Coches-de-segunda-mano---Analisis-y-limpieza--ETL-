import numpy as np
import pandas as pd

# Leemos el archivo con pandas
df = pd.read_csv("../datos/coches_segunda_mano.csv")


# Transformamos la columna kilometros a tipo float
df["kilometros"] = df["kilometros"].map(
    lambda x : float(x.split()[0].replace(".", ""))
    )

# Transformamos la columna precio a tipo float
df["precio"] = df["precio"].map(
    lambda x : float(x.split()[0].replace(".", ""))
    )

# Transformamos la columna deposito a tipo float
df["deposito"] = df["deposito"].map(
    lambda x : float(x.split()[0].replace(",", "."))
    )

# Transformamos la columna co2 a tipo float, gestionando los valores no numéricos
df["co2"] = df["co2"].map(
    lambda x : float(x.replace(",", ".")) if x.isnumeric() else np.nan
    )

df["co2"] = df.co2.fillna(round(df["co2"].mean(), 2))


# Separamos la columna fecha_matriculacion en dos columnas: month y year
mes = df["fecha_matriculacion"].map(
    lambda x : int(x.split("/")[0])
    )
anyo = df["fecha_matriculacion"].map(
    lambda x : int(x.split("/")[1])
    )

# Insertamos las nuevas columnas al principio del DataFrame
df.insert(0, 'month', mes)
df.insert(1, 'year', anyo)

# Eliminamos la columna fecha_matriculacion
df = df.drop("fecha_matriculacion", axis=1)

# Limpiamos la columna garantia
df["garantia"] = df["garantia"].map(
    lambda x: x.split()[0]
    )
df["garantia"] = df["garantia"].replace({"Sí": np.nan, "No": 0})

df["garantia"]= df["garantia"].fillna(round(df["garantia"].astype("float").mean(), 2))


# Guardamos el DataFrame limpio en un nuevo archivo CSV
df.to_csv("../datos/coches_segunda_mano_limpio.csv", index = False)