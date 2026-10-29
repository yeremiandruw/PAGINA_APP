import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página web
st.set_page_config(page_title="Optimizador de Redes - Dashboard", layout="wide", initial_sidebar_state="expanded")

# Estilo visual limpio
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1f4e79; }
    </style>
""", unsafe_allow_html=True)

st.title("🌐 Panel Interactivo de Optimización de Redes")
st.markdown("Herramienta interactiva para simular y calcular el volumen de transferencia de datos mediante cálculo integral.")

# --- BARRA LATERAL PARA CONTROLES ---
st.sidebar.header("⚙️ Controles de Simulación")
st.sidebar.markdown("Modifica las velocidades base para ver el comportamiento en tiempo real.")

# Valores base del informe
default_speeds = [42, 45, 48, 50, 47, 40, 35, 38, 44, 52, 58, 55, 49]
horas_etiquetas = [f"{i}:00 h" for i in range(8, 21)]

v_ingresadas = []
st.sidebar.subheader("Velocidad por Hora (Mbps)")
for i, h in enumerate(horas_etiquetas):
    val = st.sidebar.slider(f"{h}", min_value=10.0, max_value=100.0, value=float(default_speeds[i]), step=1.0)
    v_ingresadas.append(val)

t = np.arange(len(horas_etiquetas))
v = np.array(v_ingresadas)

# --- CÁLCULOS MATEMÁTICOS ---
h_paso = 1.0
# Trapecio
trapecio_mb = h_paso * (np.sum(v) - 0.5 * v[0] - 0.5 * v[-1]) * 3600 / 8
# Simpson 1/3
simpson_mb = (h_paso / 3) * (v[0] + v[-1] + 4 * np.sum(v[1:-1:2]) + 2 * np.sum(v[2:-2:2])) * 3600 / 8

# --- DISEÑO PRINCIPAL EN PESTAÑAS (TABS) ---
tab1, tab2, tab3 = st.tabs(["📊 Gráfica y Resultados", "📈 Comparativo por Franjas", "💡 Recomendaciones"])

with tab1:
    st.subheader("Volumen Acumulado de Datos en el Día")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Método del Trapecio", f"{trapecio_mb:,.0f} MB", f"{trapecio_mb/1024:.2f} GB", delta_color="normal")
    with col2:
        st.metric("Regla de Simpson 1/3", f"{simpson_mb:,.0f} MB", f"{simpson_mb/1024:.2f} GB", delta_color="normal")
    with col3:
        st.metric("Velocidad Promedio", f"{np.mean(v):.2f} Mbps")

    st.markdown("---")
    st.subheader("Comportamiento Dinámico de la Red $v(t)$")
    
    # Gráfica interactiva limpia
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(horas_etiquetas, v, marker='o', color='#1f4e79', linewidth=2.5, label='Velocidad Registrada')
    ax.fill_between(horas_etiquetas, v, color='#1f4e79', alpha=0.15)
    ax.set_xlabel("Hora del Día", fontweight='bold')
    ax.set_ylabel("Velocidad (Mbps)", fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.subheader("Análisis por Franjas Horarias")
    
    v_manana = v[0:5]
    mb_manana = h_paso * (np.sum(v_manana) - 0.5 * v_manana[0] - 0.5 * v_manana[-1]) * 3600 / 8
    
    v_tarde = v[4:9]
    mb_tarde = h_paso * (np.sum(v_tarde) - 0.5 * v_tarde[0] - 0.5 * v_tarde[-1]) * 3600 / 8
    
    v_noche = v[8:13]
    mb_noche = h_paso * (np.sum(v_noche) - 0.5 * v_noche[0] - 0.5 * v_noche[-1]) * 3600 / 8

    df_franjas = pd.DataFrame({
        "Franja Horaria": ["Mañana (8:00 - 12:00)", "Tarde (12:00 - 16:00)", "Noche (16:00 - 20:00)"],
        "Volumen Total (MB)": [f"{mb_manana:,.0f}", f"{mb_tarde:,.0f}", f"{mb_noche:,.0f}"],
        "Velocidad Promedio (Mbps)": [f"{np.mean(v_manana):.2f}", f"{np.mean(v_tarde):.2f}", f"{np.mean(v_noche):.2f}"]
    })
    st.table(df_franjas)

with tab3:
    st.subheader("Propuestas de Optimización basadas en el Cálculo Integral")
    st.info("📌 **Hallazgo:** La franja de la tarde muestra una caída notable en la transferencia de datos en comparación con la noche.")
    st.success("✅ **Recomendación 1:** Programar las descargas masivas o respaldos en la nube durante las horas de menor congestión.")
    st.success("✅ **Recomendación 2:** Utilizar la velocidad promedio calculada mediante integrales para negociar mejores planes con el proveedor de internet.")