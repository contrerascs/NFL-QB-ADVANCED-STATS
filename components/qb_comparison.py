import streamlit as st
import pandas as pd
import plotly.express as px
from helpers.utils import get_image_path
from helpers.utils import teams

def render_player_info(qb_id):
    # Renderiza la información del jugador en la barra lateral.
    image_path = get_image_path(qb_id)
    st.image(image_path, width=150)

def render_teams_info(qb_id, qb_data, name):
    st.subheader(":gray[Player]", divider="gray")
    st.text(name)
    st.subheader(":gray[Teams]", divider="gray")
    for team in teams(qb_id, qb_data):
        st.text(team)

def display_qb_comparison(qb_data, selected_qbs):
    # Muestra la comparación de QBs seleccionados.    
    if len(selected_qbs) == 2:
        qb1, qb2 = selected_qbs
        st.header(f'Advanced stats {qb1} and {qb2} since 2018')

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            qb1_data = qb_data[qb_data["Player"] == qb1]
            qb1_id = qb1_data["Player-additional"].iloc[0]
            render_player_info(qb1_id)

        with col2:
            render_teams_info(qb1_id,qb1_data,qb1)

        with col3:
            st.image('assets/versus.png', use_container_width=True)

        with col4:
            qb2_data = qb_data[qb_data["Player"] == qb2]
            qb2_id = qb2_data["Player-additional"].iloc[0]
            render_teams_info(qb2_id,qb2_data,qb2)

        with col5:
            render_player_info(qb2_id)
