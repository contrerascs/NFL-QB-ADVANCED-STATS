import streamlit as st

from helpers.utils import get_image_path
from helpers.utils import teams
from components.season_plots import comparative_plots

def render_player_info(qb_id):
    # Renderiza la información del jugador en la barra lateral.
    image_path = get_image_path(qb_id)
    st.image(image_path, width=150)

def render_teams_info(qb_id, qb_data, name, color):
    st.subheader(f":{color}[Player]", divider=color)
    st.text(name)
    st.subheader(f":{color}[Team]", divider=color)
    for team in teams(qb_id, qb_data):
        st.text(team)

def calculate_position(qb_data, player, metric):
    qb_data = qb_data[qb_data["Att"] > 110]
    qb_data = qb_data.sort_values(by=metric, ascending=False).reset_index(drop=True)
    qb_data[metric + "_rank"] = qb_data[metric].rank(method="min", ascending=False)
    return qb_data.loc[qb_data["Player"] == player, metric + "_rank"].values[0]

def qb_rank_in_stat(qb_df, player, stat):
    qb_data = qb_df[qb_df["Player"] == player]
    if stat == 'Cmp%' or stat == 'Rate':
        stat_value = float(qb_data[stat].iloc[0])
    elif stat == 'Y/G':
        stat_value = float(qb_data[stat].sum())
    else:
        stat_value = int(qb_data[stat].sum())

    titulos = {
        'Att':'Atts',
        'Cmp%':'Cmp%',
        'Yds': 'Air Yds',
        'TD':'Touchdowns',
        'Int':'Ints',
        'Rate':'Rating'
    }

    rank = calculate_position(qb_df, player, stat)
    if stat == 'Int':
        if rank > 20:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º",border=True)
        elif rank > 10:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º", "off",border=True)
        else:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º","inverse",border=True)
    else:
        if rank > 20:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º","inverse",border=True)
        elif rank > 10:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º", "off",border=True)
        else:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º",border=True)

def display_qb_comparison(qb_data, selected_qb1, selected_qb2):
    # Muestra la comparación de QBs seleccionados.    
    qb1 = selected_qb1
    qb2 = selected_qb2
    st.header(f'Advanced stats {qb1} and {qb2} since 2018')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        qb1_data = qb_data[qb_data["Player"] == qb1]
        qb1_id = qb1_data["Player-additional"].iloc[0]
        render_player_info(qb1_id)

    with col2:
        render_teams_info(qb1_id,qb1_data,qb1,'red')

    with col3:
        st.image('assets/versus.png', use_container_width=True)

    with col4:
        qb2_data = qb_data[qb_data["Player"] == qb2]
        qb2_id = qb2_data["Player-additional"].iloc[0]
        render_teams_info(qb2_id,qb2_data,qb2,'blue')

    with col5:
        render_player_info(qb2_id)

    stats = ['Att',"Cmp%","Yds","TD","Int", "Rate"]
    stat_labels = ['Atts',"%Completos","Air Yards","Touchdowns","Interceptions","Rating"]
        
    for stat, label in zip(stats, stat_labels):
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
            
        with col1:
            qb_rank_in_stat(qb_data,qb1,stat)
            
        with col2:
            fig = comparative_plots(qb1,qb2,stat,label,qb_data)
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
            qb_rank_in_stat(qb_data,qb2,stat)