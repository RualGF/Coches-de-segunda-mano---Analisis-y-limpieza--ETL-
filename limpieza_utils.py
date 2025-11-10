import numpy as np
import pandas as pd

def limpiar_kilometros(df_entrada):
    df = df_entrada.copy()
    df["kilometros"] = pd.to_numeric(df["kilometros"].str.replace(".", "", regex=False).str.split().str[0], errors="coerce")
    return df

def limpiar_precio(df_entrada):
    df = df_entrada.copy()
    df["precio"] = pd.to_numeric(df["precio"].str.replace(".", "", regex=False).str.split().str[0], errors="coerce")
    return df

def limpiar_deposito_co2(df_entrada):
    df = df_entrada.copy()
    df["deposito"] = pd.to_numeric(df["deposito"].str.replace(",", ".", regex=False), errors="coerce")
    df["co2"] = pd.to_numeric(df["co2"].str.replace(",", ".", regex=False), errors="coerce")
    if df["co2"].isnull().any():
        df["co2"] = df["co2"].fillna(round(df["co2"].mean(), 2))
    return df

def separar_fecha(df_entrada):
    df = df_entrada.copy()
    if "fecha_matriculacion" in df.columns:
        fecha_split = df["fecha_matriculacion"].str.split("/", expand=True)
        df.insert(0, 'month', pd.to_numeric(fecha_split[0], errors='coerce'))
        df.insert(1, 'year', pd.to_numeric(fecha_split[1], errors='coerce'))
        df.drop("fecha_matriculacion", axis=1, inplace=True)
    return df

def limpiar_garantia(df_entrada):
    df = df_entrada.copy()
    df["garantia"] = df["garantia"].str.replace(" meses", "", regex=False)
    df["garantia"] = df["garantia"].replace({"Sí": np.nan, "No": "0"})
    df["garantia"] = pd.to_numeric(df["garantia"], errors="coerce")
    if df["garantia"].isnull().any():
        df["garantia"] = df["garantia"].fillna(round(df["garantia"].mean(), 2))
    return df

def limpiar_dataframe_completo(df_entrada):
    """Aplica todos los pasos de limpieza en secuencia."""
    df = df_entrada.copy()
    df = limpiar_kilometros(df)
    df = limpiar_precio(df)
    df = limpiar_deposito_co2(df)
    df = separar_fecha(df)
    df = limpiar_garantia(df)
    return df

def main():
    """Función para ejecutar el script de forma independiente."""
    df_sin_limpiar = pd.read_csv("datos/coches_segunda_mano.csv")
    df_limpio = limpiar_dataframe_completo(df_sin_limpiar)
    df_limpio.to_csv("datos/coches_segunda_mano_limpio.csv", index=False)
    print("Archivo 'coches_segunda_mano_limpio.csv' generado correctamente.")

if __name__ == "__main__":
    main()
