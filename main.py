import streamlit as st
from helpers.data_loader import load_dataset
from components.qb_comparison import display_qb_comparison
from components.sidebar import render_sidebar

# Configuración inicial de Streamlit
st.set_page_config(
    page_title='QB vs QB',
    page_icon=':football:',
    layout='wide',
    initial_sidebar_state='expanded',
)

df = load_dataset()

# Capturar selección del usuario
selected_qb1, selected_qb2, selected_season = render_sidebar(df)

# Filtrar DataFrame por la temporada seleccionada
df_season = df[df['Season'] == selected_season]

# Verificar si los jugadores están en la temporada seleccionada
qb1_exists = selected_qb1 in df_season['Player'].values
qb2_exists = selected_qb2 in df_season['Player'].values

if not qb1_exists or not qb2_exists:
    # Mostrar advertencias si un jugador no jugó en la temporada seleccionada
    if not qb1_exists:
        st.warning(f"⚠️ {selected_qb1} not played in season {selected_season}.")
    if not qb2_exists:
        st.warning(f"⚠️ {selected_qb2} not played in season {selected_season}.")
else:
    # Mostrar comparación solo si ambos jugadores jugaron en la temporada seleccionada
    display_qb_comparison(df_season, selected_qb1, selected_qb2)
