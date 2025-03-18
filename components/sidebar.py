import streamlit as st

def render_sidebar(df):
    """Renderiza la barra lateral completa."""
    with st.sidebar:
        st.image('assets/sam_logo.png',use_container_width=True)

        # Obtener lista de QBs
        qb_list = df["Player"].unique().tolist()

        # Selección de QBs con st.multiselect()
        selected_qbs = st.multiselect("Selecciona 2 QBs para comparar", qb_list, default=qb_list[:2])

    return selected_qbs