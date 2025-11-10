# 🚗 Análisis Interactivo de Coches de Segunda Mano

Este proyecto es una aplicación web interactiva construida con Streamlit para la limpieza y el análisis de un conjunto de datos de coches de segunda mano.

La aplicación permite visualizar el proceso de transformación de datos paso a paso y explorar los análisis resultantes a través de una interfaz amigable.

## 🚀 Características

La aplicación se divide en cuatro secciones principales:

1.  **🏠 Inicio:** Una página de bienvenida que introduce el proyecto.
2.  **1️⃣ Limpieza:** Un dashboard que muestra el "antes" y el "después" de cada paso del proceso de limpieza de datos. Permite descargar el dataset limpio (`.csv`) una vez procesado.
3.  **2️⃣ Análisis:** Un dashboard que presenta varias métricas y análisis sobre los datos ya limpios, como estadísticas descriptivas, distribuciones por año, precios medios, etc.
4.  **3️⃣ EDA:** Una página dedicada al Análisis Exploratorio de Datos (EDA) con visualizaciones interactivas, incluyendo un mapa de correlación.

## 📂 Estructura del Proyecto

```
.
├── datos/
│   ├── coches_segunda_mano.csv           # Dataset original
│   └── coches_segunda_mano_limpio.csv    # Dataset generado por el script/app
├── pages/
│   ├── 1_Limpieza.py                     # Script de la página de limpieza
│   ├── 2_Análisis.py                     # Script de la página de análisis
│   └── 3_EDA.py                          # Script de la página de EDA
├── scripts/
│   ├── analisis.py                       # Script original de análisis (no interactivo)
│   └── limpieza.py                       # Script original de limpieza (no interactivo)
├── Inicio.py                             # Script principal para lanzar la app
├── limpieza_utils.py                     # Módulo con las funciones de limpieza
├── requirements.txt                      # Dependencias del proyecto
└── README.md                             # Este archivo
```

## 🛠️ Instalación

Se recomienda utilizar un entorno virtual para gestionar las dependencias.

1.  **Clona o descarga el repositorio.**

2.  **Crea y activa un entorno virtual (opcional pero recomendado):**
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    El proyecto utiliza las librerías listadas en `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Cómo Ejecutar la Aplicación

Una vez instaladas las dependencias, ejecuta el siguiente comando desde la carpeta raíz del proyecto:

```bash
streamlit run Inicio.py
```

Se abrirá una nueva pestaña en tu navegador con la aplicación web.
