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

selected_qbs,selected_season = render_sidebar(df)

df_season = df[df['Season'] == selected_season[0]]
print(df_season)

if len(selected_qbs) == 2:
    display_qb_comparison(df_season[df_season["Player"].isin(selected_qbs)], selected_qbs)
else:
    st.warning("⚠️ Por favor selecciona exactamente 2 jugadores.")