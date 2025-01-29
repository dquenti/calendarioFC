import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

# Deshabilitar warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning, message="missing ScriptRunContext")

# Título de la aplicación
st.title("FONDOS CONCURSABLES - CALENDARIO 🗓️")

# Leer el archivo Excel
df = pd.read_excel("Fondos_c.xlsx", sheet_name="AT Planning")

# Convertir las columnas de fechas a tipo datetime
df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
df["End Date"] = pd.to_datetime(df["End Date"], errors="coerce")

# Verificar si hay fechas no válidas
if df["Start Date"].isnull().any() or df["End Date"].isnull().any():
    st.warning("Algunas fechas no pudieron ser convertidas. Por favor, verifica el formato de las fechas en el archivo Excel.")

# Definir un mapeo de colores para los estados
color_discrete_map = {
    "proceso abierto": "green",  # Color para proceso abierto
    "proceso cerrado": "red",    # Color para proceso cerrado
    "pronta apertura": "orange"  # Color para pronta apertura
}

# Modificar los nombres de los proyectos para que aparezcan en dos líneas
df["Project step"] = df["Project step"].apply(lambda x: x.replace(" ", "\n"))  # Insertar saltos de línea

# Crear el gráfico de Gantt con Plotly
st.write(" ")
fig = px.timeline(
    df,
    x_start="Start Date",
    x_end="End Date",
    y="Project step",
    title="",
    labels={"Project step": "Fondo", "Start Date": "Fecha de Inicio", "End Date": "Fecha de Fin"},
    color="Progress",  # Colorear por progreso
    hover_name="Description",  # Mostrar la descripción al pasar el mouse
    color_discrete_map=color_discrete_map  # Aplicar el mapeo de colores
)

# Ajustar el diseño del gráfico
fig.update_yaxes(autorange="reversed")  # Invertir el eje Y

# Definir el rango del eje X para mostrar todos los meses del año 2025
fig.update_layout(
    xaxis_title=None,  # Quitar el título del eje X
    yaxis_title="",
    showlegend=True,
    height=800,  # Aumentar la altura del gráfico para que las barras tengan más espacio
    margin=dict(l=50, r=50, t=80, b=200),  # Ajustar los márgenes para que los nombres de los meses no se corten
    xaxis_range=["2025-01-01", "2025-12-31"],  # Rango del eje X para todo el año 2025
    xaxis=dict(
        tickmode="array",  # Configurar los ticks manualmente
        tickvals=pd.date_range(start="2025-01-01", end="2025-12-31", freq="MS"),  # Mostrar un tick por mes
        ticktext=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],  # Nombres completos de los meses
        tickangle=-45,  # Rotar los nombres de los meses para que no se superpongan
    ),
    legend=dict(
        title=None,  # Quitar el título de la leyenda
        orientation="h",  # Leyenda horizontal
        yanchor="bottom",  # Anclar la leyenda en la parte inferior
        y=-0.3,  # Posición vertical de la leyenda (fuera del gráfico)
        xanchor="center",  # Centrar la leyenda horizontalmente
        x=0.5  # Posición horizontal de la leyenda (centrada)
    )
)

# Mostrar el gráfico en la aplicación
st.plotly_chart(fig, use_container_width=True)

# Mostrar el dataframe en la aplicación (opcional)
st.write("### Más Info")
st.dataframe(df)

# Agregar un pie de página
st.write("---")
st.write("Creado usando Streamlit y Plotly by DanielaQ")