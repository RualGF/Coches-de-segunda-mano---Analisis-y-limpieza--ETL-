import streamlit as st
import pandas as pd
import io

# Importamos CADA función de limpieza específica
from limpieza_utils import (
    limpiar_kilometros, limpiar_precio, limpiar_deposito_co2, 
    separar_fecha, limpiar_garantia, limpiar_dataframe_completo
)

# --- Configuración de la página y Título ---
st.set_page_config(page_title="Proceso de Limpieza", layout="wide")
st.title("1️⃣ Visualización del Proceso de Limpieza")
st.write(
    "Esta página muestra el efecto de cada paso de limpieza sobre el DataFrame. "
    "Usa los expanders para ver el detalle de cada transformación."
)

# --- Carga de datos ---
# Usamos una función con caché para que los datos se carguen solo una vez.
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos/coches_segunda_mano.csv")

df_original = cargar_datos()

st.header("Estado Inicial del DataFrame")
st.write(f"El DataFrame original tiene {df_original.shape[0]} filas y {df_original.shape[1]} columnas.")
if st.checkbox("Mostrar una muestra de los datos originales"):
    st.dataframe(df_original.head())


# --- PASO 1: Limpieza de 'kilometros' ---
st.header("1. Limpieza de la columna `kilometros`")
with st.expander("Ver detalles del paso 1"):
    st.write("Objetivo: Convertir '2.500 km' a un número `2500.0`.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Antes** (primeros 5 valores):")
        st.code(df_original['kilometros'].head().to_string(), language='text')
    # Aplicamos la transformación
    df_paso1 = limpiar_kilometros(df_original)
    with col2:
        st.write("**Después** (primeros 5 valores):")
        st.code(df_paso1['kilometros'].head().to_string(), language='text')
    st.success(f"Tipo de dato final: `{df_paso1['kilometros'].dtype}`")


# --- PASO 2: Limpieza de 'precio' ---
st.header("2. Limpieza de la columna `precio`")
with st.expander("Ver detalles del paso 2"):
    st.write("Objetivo: Convertir '33.400 €' a un número `33400.0`.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Antes**:")
        st.code(df_paso1['precio'].head().to_string(), language='text')
    # Aplicamos la transformación
    df_paso2 = limpiar_precio(df_paso1)
    with col2:
        st.write("**Después**:")
        st.code(df_paso2['precio'].head().to_string(), language='text')
    st.success(f"Tipo de dato final: `{df_paso2['precio'].dtype}`")


# --- PASO 3: Limpieza de 'deposito' y 'co2' ---
st.header("3. Limpieza de `deposito` y `co2`")
with st.expander("Ver detalles del paso 3"):
    st.write("Objetivo: Convertir textos con comas a números decimales y rellenar nulos.")
    # Deposito
    conteo_nan_antes = df_paso2['co2'].isnull().sum()
    st.write(f"Valores nulos antes de rellenar: **{conteo_nan_antes}**")
    df_paso3 = limpiar_deposito_co2(df_paso2)
    conteo_nan_despues = df_paso3['co2'].isnull().sum()
    st.write(f"Valores nulos después de rellenar: **{conteo_nan_despues}**")
    st.success("Columnas `deposito` y `co2` procesadas.")


# --- PASO 4: Separación de 'fecha_matriculacion' ---
st.header("4. Separación de `fecha_matriculacion`")
with st.expander("Ver detalles del paso 4"):
    st.write("Objetivo: Separar '05/2023' en dos columnas `month` (5) y `year` (2023).")
    df_paso4 = separar_fecha(df_paso3)
    st.write("Nuevas columnas creadas (`month`, `year`) y `fecha_matriculacion` eliminada.")
    st.dataframe(df_paso4[['month', 'year']].head())


# --- PASO 5: Limpieza de 'garantia' ---
st.header("5. Limpieza de la columna `garantia`")
with st.expander("Ver detalles del paso 5"):
    st.write("Objetivo: Convertir '12 meses', 'Sí' y 'No' a valores numéricos.")
    df_paso5 = limpiar_garantia(df_paso4)
    st.write("Valores transformados y nulos rellenados con la media.")
    st.dataframe(df_paso5['garantia'].head())
    st.success(f"Tipo de dato final: `{df_paso5['garantia'].dtype}`")


# --- RESULTADO FINAL ---
st.header("Resultado Final")
st.write("A continuación se muestra un resumen y una muestra del DataFrame limpio.")

# Usamos la función que aplica todos los pasos de una vez
df_limpio = limpiar_dataframe_completo(df_original)

with io.StringIO() as buffer:
    df_limpio.info(buf=buffer)
    st.code(buffer.getvalue(), language="plaintext")

st.dataframe(df_limpio.head())

# Guardamos el dataframe limpio en el estado de la sesión para que otras páginas puedan usarlo
st.session_state['df_limpio'] = df_limpio

st.success(f"¡Limpieza completada! El DataFrame final tiene {df_limpio.shape[0]} filas y {df_limpio.shape[1]} columnas.")
#st.write(f"Hemos limpiado y transformado {df_original.shape[0] - df_limpio.shape[0]} filas y {df_original.shape[1] - df_limpio.shape[1]} columnas.")

# --- Botón de descarga ---
with st.spinner("Generando archivo para descarga..."):
    csv = df_limpio.to_csv(index=False).encode('utf-8')
    st.download_button(
       label="Descargar CSV Limpio",
       data=csv,
       file_name='coches_segunda_mano_limpio.csv',
       mime='text/csv',
    )
