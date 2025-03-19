import streamlit as st

def render_sidebar(df):
    # Renderiza la barra lateral completa.
    with st.sidebar:
        st.image('assets/sam_logo.png',use_container_width=True)

        # Obtener lista de QBs
        qb_list = df["Player"].unique().tolist()

        # Obtener lista de temporadas
        season_list = df['Season'].unique().tolist()

        # Selección de QBs con st.multiselect()
        selected_qbs = st.multiselect("Selecciona 2 QBs para comparar", qb_list, default=qb_list[:2])

        # Selección de temporadas
        selected_season = st.multiselect('Selecciona las temporadas a comparar', season_list)
        print(selected_qbs,selected_season)

    return selected_qbs,selected_season