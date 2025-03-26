import streamlit as st

def render_sidebar(df):
    # Renderiza la barra lateral completa.
    with st.sidebar:
        st.image('assets/logo.png', use_container_width=True)

        # Obtener lista de temporadas ordenadas (más recientes primero)
        season_list = sorted(df["Season"].unique().tolist(), reverse=True)
        season_list = [season for season in season_list if season != 2018]
        
        # Selección de temporada primero
        selected_season = st.selectbox('Select a season', season_list, key='season')
        
        # Filtrar el dataframe por la temporada seleccionada
        season_df = df[df["Season"] == selected_season]
        
        # Obtener lista de QBs que jugaron en esa temporada
        qb_list = season_df["Player"].unique().tolist()
        
        # Verificar que haya al menos 2 QBs en la temporada seleccionada
        if len(qb_list) < 2:
            st.warning(f"¡Solo hay {len(qb_list)} QB(s) en la temporada {selected_season}!")
            if len(qb_list) == 1:
                return qb_list[0], None, selected_season
            else:
                return None, None, selected_season
        
        # Selección del primer QB
        selected_qb1 = st.selectbox("Select a quarterback", qb_list, key='qb1')
        
        # Filtrar la lista para el segundo selectbox (excluyendo el primero)
        qb_list_filtered = [qb for qb in qb_list if qb != selected_qb1]
        
        # Selección del segundo QB (sin incluir el primero seleccionado)
        selected_qb2 = st.selectbox("Select a quarterback", qb_list_filtered, key='qb2')

    return selected_qb1, selected_qb2, selected_season