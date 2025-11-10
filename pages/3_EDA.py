import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("Análisis Exploratorio de Datos (EDA)")

df = pd.read_csv("datos/coches_segunda_mano_limpio.csv")

#01 Columna precio
st.header("01. Columna: Precio")

fig_precio = make_subplots(rows=1, cols=2, subplot_titles=("Histograma de Precio", "Histograma de Log Precio"))

fig_precio.add_trace(go.Histogram(x=df["precio"], name="Precio", marker_color="green"), row=1, col=1)

df["log_precio"] = np.log(df["precio"])

fig_precio.add_trace(go.Histogram(x=df["log_precio"], name="Log Precio", marker_color="magenta"), row=1, col=2)

fig_precio.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_precio, width='stretch')

#02 Columna kilómetros
st.header("02. Columna: Kilómetros")

std = np.std(df["kilometros"])

fig_km = px.histogram(df, x="kilometros", color_discrete_sequence=["green"], title="Histograma de Kilómetros")
fig_km.add_vline(x=std, line_color="red", line_dash="dash", annotation_text="1*std")
fig_km.add_vline(x=std * 2, line_color="red", line_dash="dash", annotation_text="2*std")
fig_km.add_vline(x=std * 3, line_color="red", line_dash="dot", annotation_text="3*std")
st.plotly_chart(fig_km, width='stretch')

# 03 Filtrado de Datos
st.header("03. Filtrado de Datos")

std_precio = np.std(df["precio"])
std_km = np.std(df["kilometros"])

df = df[(df["precio"] <= (std_precio * 3)) & (df["kilometros"] <= (std_km * 4))]
st.write(f"DataFrame filtrado por precio (menor o igual a {std_precio * 3:.2f}) y kilómetros (menor o igual a {std_km * 4:.2f}).")

filtro = df.value_counts("tipo_combustible", ascending = True).head(3).index.to_list()
df = df[~df["tipo_combustible"].isin(filtro)]
st.write(f"Se han eliminado las 3 categorías de tipo de combustible menos frecuentes: {', '.join([f"'{item}'" for item in filtro])}.")

df = df[(df["deposito"] > 0) & (df["peso_masa_kg"] > 0)]
st.write("Se han filtrado los datos donde 'deposito' y 'peso_masa_kg' son mayores que 0.")

#04 Columnas: distintivo_ambiental y precio
st.header("04. Columnas: Distintivo Ambiental y Precio")
fig_distintivo_precio = make_subplots(rows=1, cols=2, subplot_titles=("Boxplot de Precio por Distintivo Ambiental", "Boxplot de Log Precio por Distintivo Ambiental"))

fig_distintivo_precio.add_trace(go.Box(x=df["distintivo_ambiental"], y=df["precio"], name="Precio", marker_color="green"), row=1, col=1)
fig_distintivo_precio.add_trace(go.Box(x=df["distintivo_ambiental"], y=df["log_precio"], name="Log Precio", marker_color="magenta"), row=1, col=2)

fig_distintivo_precio.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_distintivo_precio, width='stretch')

# 05 Columnas: tipo_combustible, tipo_cambio y precio:
st.header("05. Columnas: Tipo de Combustible, Tipo de Cambio y Precio")

# Barplot
fig_bar = px.bar(df, x="tipo_cambio", color="tipo_combustible", title="Distribución de Tipo de Combustible por Tipo de Cambio")
st.plotly_chart(fig_bar, width='stretch')

# Boxplot
fig_box = px.box(df, x="precio", y="tipo_combustible", color="tipo_cambio", title="Boxplot de Precio por Tipo de Combustible y Tipo de Cambio")
st.plotly_chart(fig_box, width='stretch')

#06 Columnas: peso_masa_kg, co2 y distintivo_ambiental
st.header("06. Columnas: Peso, CO2 y Distintivo Ambiental")
fig_peso_co2 = px.scatter(data_frame = df, x = "peso_masa_kg", y = "co2", color = "distintivo_ambiental", hover_data = df.columns, title="Relación entre Peso, CO2 y Distintivo Ambiental")
st.plotly_chart(fig_peso_co2, width='stretch')

st.write("""
La relación entre las tres columnas es que entre los coches con distintivos C y B, con un peso de entre unos 1500 y 2750 kg, emiten más o menos las mismas emisiones de co2.
A destacar también que los coches con distintivos "0 emisiones" pesan entre 1700 y 3300 kg, y todos emiten más de 0 emisiones de co2.
""")

#07 Correlación
st.header("07. Correlación")

# Seleccionar solo columnas numéricas y limpiar NaN/inf para la correlación
df_numeric = df.select_dtypes(include=np.number)
df_numeric = df_numeric.replace([np.inf, -np.inf], np.nan) # Reemplazar infinitos con NaN
df_numeric = df_numeric.fillna(df_numeric.mean()) # Rellenar NaN con la media de la columna

fig_corr = px.imshow(df_numeric.corr().round(2), text_auto=True, aspect="auto", title="Mapa de Calor de Correlación")
st.plotly_chart(fig_corr, width='stretch')