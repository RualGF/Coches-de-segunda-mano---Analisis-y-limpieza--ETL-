import streamlit as st

st.set_page_config(
    page_title="Análisis de Coches de Segunda Mano",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Análisis de Coches de Segunda Mano")

st.write("""
¡Bienvenido al dashboard de análisis de coches de segunda mano!

Esta aplicación te permite explorar el proceso completo, desde la limpieza inicial de los datos hasta el análisis final.
""")

st.info("""
**Navega por las páginas en el menú de la izquierda para comenzar:**

*   **1️⃣ Limpieza:** Visualiza el 'antes' y el 'después' de cada transformación de datos.
*   **2️⃣ Análisis:** Explora los resultados y las conclusiones obtenidas a partir de los datos limpios.
""")
