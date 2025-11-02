import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análisis de datos", layout="wide", page_icon="📊")

st.title("2️⃣ Análisis sobre los datos limpios")

@st.cache_data
def cargar_csv():
    """Carga los datos desde el archivo CSV como último recurso."""
    try:
        df = pd.read_csv("datos/coches_segunda_mano_limpio.csv")
        return df
    except FileNotFoundError:
        return None


if 'df_limpio' in st.session_state:
    # 1. Usamos el DataFrame del estado de la sesión si existe (más rápido)
    st.info("Cargando datos limpios desde la sesión actual.")
    df_limpio = st.session_state['df_limpio']
else:
    # 2. Si no, intentamos cargarlo desde el archivo CSV
    st.info("No se encontraron datos en la sesión. Intentando cargar desde 'coches_segunda_mano_limpio.csv'...")
    df_limpio = cargar_csv()

if df_limpio is not None:
    st.header("1. Estadísticos Descriptivos")
    st.dataframe(df_limpio.describe())

    st.header("2. Porcentaje de coches matriculados por año")
    porcentaje_coches_por_anyo = (df_limpio['year'].value_counts(normalize=True) * 100).round(2).astype(str) + ' %'
    st.dataframe(porcentaje_coches_por_anyo.rename("Porcentaje"))

    st.header("3. Porcentaje de coches con potencia mayor a la media")
    media = df_limpio["potencia_cv"].mean()
    st.write(f"La potencia media es de **{media:.2f} CV**.")
    porcentaje_potencia = (df_limpio[df_limpio['potencia_cv'] > media]['potencia_cv'].value_counts(normalize=True) * 100).round(2).astype(str) + ' %'
    st.dataframe(porcentaje_potencia.rename("Porcentaje"))

    st.header("4. Combustibles menos comunes")
    combustibles_raros = df_limpio['tipo_combustible'].value_counts().sort_values(ascending=True).head(3)
    st.table(combustibles_raros.rename("Cantidad"))

    st.header("5. Distintivo ambiental con el precio medio más alto")
    precio_por_distintivo = df_limpio.groupby("distintivo_ambiental")[["precio"]].mean().sort_values(by="precio", ascending=False)
    st.dataframe(precio_por_distintivo)

    st.header("6. Año con la menor emisión media de CO2")
    co2_por_anyo = df_limpio.groupby("year")[["co2"]].mean().sort_values(by="co2", ascending=True)
    st.table(co2_por_anyo.head(1))
else:
    st.error("No se pudieron cargar los datos limpios. Por favor, ve a la página '1️⃣ Limpieza' y ejecuta el proceso primero.")
    st.warning("Si el archivo `coches_segunda_mano_limpio.csv` ya existe en la carpeta, asegúrate de que la aplicación tiene permisos para leerlo.")