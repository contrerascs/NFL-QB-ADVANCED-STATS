import streamlit as st
import pandas as pd

from helpers.utils import get_image_path
from helpers.utils import teams
from components.season_plots import comparative_plots, plot_radar_chart, plot_indicator, bar_plots, stacked_bar, plot_indicator_accuracy
from helpers.utils import normalize, invert_normalize

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

def calculate_qb_skills(df):
    # Calcula las 7 habilidades de los quarterbacks en una escala de 1 a 100.
    skills = pd.DataFrame()
    skills['Player'] = df['Player']
    
    # Protección del balón (Ball Security)
    skills['Ball Security'] = (invert_normalize(df['Int']) + 
                               invert_normalize(df['Int%']) + 
                               invert_normalize(df['BadTh']) + 
                               invert_normalize(df['Bad%'])) / 4
    
    # Precisión (Accuracy)
    skills['Accuracy'] = (normalize(df['Cmp%']) + 
                          normalize(df['OnTgt%']) + 
                          invert_normalize(df['Drop%'])) / 3
    
    # Eficiencia en el pase (Passing Efficiency)
    skills['Passing Efficiency'] = (normalize(df['Y/A']) + 
                                    normalize(df['AY/A']) + 
                                    normalize(df['ANY/A']) + 
                                    normalize(df['Rate'])) / 4
    
    # Juego bajo presión (Pocket Performance)
    skills['Pocket Performance'] = (invert_normalize(df['Prss%']) + 
                                    invert_normalize(df['Hrry']) + 
                                    invert_normalize(df['Hits']) + 
                                    invert_normalize(df['Sk%'])) / 4
    
    # Capacidad de jugadas explosivas (Big Play Ability)
    skills['Big Plays'] = (normalize(df['IAY']) + 
                                  normalize(df['IAY/PA']) + 
                                  normalize(df['CAY']) + 
                                  normalize(df['CAY/PA']) + 
                                  normalize(df['Lng'])) / 5
    
    # Movilidad (Mobility & Scrambling)
    skills['Mobility'] = (normalize(df['Scrm']) + 
                          normalize(df['Yds/Scr']) + 
                          normalize(df['PktTime']) + 
                          normalize(df['RPO_RushYds'].fillna(0))) / 4
    
    # Eficiencia en zona roja (Red Zone Efficiency)
    skills['Red Zone Efficiency'] = (normalize(df['Inside_20_Cmp%']) + 
                                     normalize(df['Inside_20_TD']) + 
                                     normalize(df['Inside_10_Cmp%']) + 
                                     normalize(df['Inside_10_TD'])) / 4
    
    return skills

def display_qb_comparison(qb_data, selected_qb1, selected_qb2):
    # Muestra la comparación de QBs seleccionados.    
    qb1 = selected_qb1
    qb2 = selected_qb2
    season = qb_data['Season'].iloc[0]
    st.header(f'Advanced stats {qb1} and {qb2} in {season}')

    col1, col2, col3 = st.columns([1,5,1])

    with col1:
        qb1_data = qb_data[qb_data["Player"] == qb1]
        qb1_id = qb1_data["Player-additional"].iloc[0]
        render_player_info(qb1_id)
        render_teams_info(qb1_id,qb1_data,qb1,'red')

    with col2:
        data_skills = calculate_qb_skills(qb_data)
        fig1 = plot_radar_chart(data_skills, qb1, qb2)
        st.plotly_chart(fig1, use_container_width=True)

    with col3:
        qb2_data = qb_data[qb_data["Player"] == qb2]
        qb2_id = qb2_data["Player-additional"].iloc[0]
        render_player_info(qb2_id)
        render_teams_info(qb2_id,qb2_data,qb2,'blue')

    stats = ['Att',"Cmp%","Yds","TD","Int", "Rate"]
    stat_labels = ['Atts',"%Completos","Air Yards","Touchdowns","Interceptions","Rating"]
        
    for stat, label in zip(stats, stat_labels):
        col1, col2, col3 = st.columns([1, 5, 1])
            
        with col1:
            qb_rank_in_stat(qb_data,qb1,stat)
            
        with col2:
            fig = comparative_plots(qb1,qb2,stat,label,qb_data)
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
            qb_rank_in_stat(qb_data,qb2,stat)

    c1, c2 = st.columns(2)

    with c1:
        delta = calculate_position(qb_data, qb1, 'Rate')
        fig_indicator1 = plot_indicator(qb1_data,qb1,'red',delta)
        st.plotly_chart(fig_indicator1, use_container_width=True)

    with c2:
        delta = calculate_position(qb_data, qb2, 'Rate')
        fig_indicator2 = plot_indicator(qb2_data,qb2,'darkblue',delta)
        st.plotly_chart(fig_indicator2, use_container_width=True)

    fig_bar = bar_plots(qb_data,qb1,qb2)
    st.plotly_chart(fig_bar,use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        delta = calculate_position(qb_data, qb1, 'OnTgt%')
        fig_indicator1 = plot_indicator_accuracy(qb1_data,qb1,'red',delta)
        st.plotly_chart(fig_indicator1, use_container_width=True)

    with c2:
        delta = calculate_position(qb_data, qb2, 'OnTgt%')
        fig_indicator2 = plot_indicator_accuracy(qb2_data,qb2,'darkblue',delta)
        st.plotly_chart(fig_indicator2, use_container_width=True)

    fig_stacked_bar = stacked_bar(qb_data,qb1,qb2)
    st.plotly_chart(fig_stacked_bar,use_container_width=True)