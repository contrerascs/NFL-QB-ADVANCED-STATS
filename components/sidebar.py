import streamlit as st

def render_sidebar(df):
    # Renderiza la barra lateral completa.
    with st.sidebar:
        st.image('assets/sam_logo.png',use_container_width=True)

        # Obtener lista de QBs
        qb_list = df["Player"].unique().tolist()

        # Obtener lista de temporadas
        season_list = ["Since 2018"] + sorted(df["Season"].unique().tolist(), reverse=True)

        # Selección del primer QB
        selected_qb1 = st.selectbox("Selecciona el QB a comparar", qb_list, key='qb1')

        # Filtrar la lista para el segundo selectbox
        qb_list_filtered = [qb for qb in qb_list if qb != selected_qb1]

        # Selección del segundo QB (sin incluir el primero seleccionado)
        selected_qb2 = st.selectbox("Selecciona el QB a comparar", qb_list_filtered, key='qb2')

        # Selección de temporadas
        selected_season = st.selectbox('Selecciona las temporadas a comparar', season_list)

    return selected_qb1, selected_qb2 ,selected_season