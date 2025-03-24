import plotly.graph_objects as go
import numpy as np

def comparative_plots(qb1,qb2,stat,label,qb_data):
    qb1_data = qb_data[qb_data["Player"] == qb1]
    qb2_data = qb_data[qb_data["Player"] == qb2]

    qb1_value = qb1_data[stat].iloc[0]
    qb2_value = qb2_data[stat].iloc[0]

    # Crear una figura con un gráfico de lollipop
    fig = go.Figure()

    # Línea y punto para qb1
    fig.add_trace(go.Scatter(
        x=[qb1_value, qb1_value],
        y=[label, label],
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(color='red', size=10),
        name=qb1
        ))

    # Línea y punto para qb2
    fig.add_trace(go.Scatter(
        x=[qb2_value, qb2_value],
        y=[label, label],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(color='blue', size=10),
        name=qb2
        ))

    # Ajustar el layout
    fig.update_layout(
        showlegend=False,
        #xaxis_title=label,
        yaxis_title="",
        height=100,  # Altura compacta
        margin=dict(l=20, r=20, t=20, b=20),
        )

    return fig

def plot_radar_chart(df, qb1, qb2):
    skills = ["Ball Security", "Passing Efficiency", "Accuracy","Mobility", "Big Plays", "Pocket Performance" , "Red Zone Efficiency"]
    
    qb1_stats = df[df["Player"] == qb1][skills].values.flatten()
    qb2_stats = df[df["Player"] == qb2][skills].values.flatten()
    
    categories = skills + [skills[0]]
    
    qb1_stats = np.append(qb1_stats, qb1_stats[0])
    qb2_stats = np.append(qb2_stats, qb2_stats[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=qb1_stats,
        theta=categories,
        fill='toself',
        name=qb1,
        line_color='red'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=qb2_stats,
        theta=categories,
        fill='toself',
        name=qb2,
        line_color='blue'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 100])
            ),
        showlegend=False,
        #title=f'Comparación de {qb1} vs {qb2} en {season}',
        template='plotly_dark'
    )
    
    return fig

def plot_indicator(data,qb,color,reference_value):
    rate = data['Rate'].iloc[0]
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = rate,
        delta={'reference': (rate-reference_value)},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 158.3], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 100], 'color': 'black'},
                {'range': [100, 158.3], 'color': 'black'}
            ],
            'threshold': {
                #'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 158.3
            }
        }
    ))

    fig.update_layout(
        title=f"{qb} Quarterback Rating",
        template="plotly_dark",
        width=400,  # Ajusta el ancho en píxeles
        height=400
    )

    return fig

def bar_plots(df,qb1,qb2):
    # Definir las métricas de Red Zone
    red_zone_metrics = [
        "Inside_20_Att", "Inside_20_Cmp", "Inside_20_Cmp%",
        "Inside_20_TD", "Inside_10_Att", "Inside_10_Cmp", 
        "Inside_10_Cmp%", "Inside_10_TD", "Inside_20_Int"
    ]

    # Crear una lista de nombres formateados para el eje x
    formatted_metrics = [
        "Atts Inside 20", "Cmp Inside 20", "Cmp% Inside 20",
        "TD's Inside 20", "Att Inside 10", "Cmp Inside 10", 
        "Cmp% Inside 10", "Td's Inside 10", "Ints in Red Zone"
    ]

    # Extraer datos de los dos QB seleccionados
    qb1_stats = df[df["Player"] == qb1][red_zone_metrics].values[0]
    qb2_stats = df[df["Player"] == qb2][red_zone_metrics].values[0]

    # Crear la gráfica de barras
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=formatted_metrics,
        y=qb1_stats,
        name=qb1,
        marker_color="red"
    ))

    fig.add_trace(go.Bar(
        x=formatted_metrics,
        y=qb2_stats,
        name=qb2,
        marker_color="blue"
    ))

    # Personalización del diseño
    fig.update_layout(
        title=f"Red Zone Performance Comparison: {qb1} vs {qb2}",
        xaxis_title="Metrics",
        barmode="group",  # Barras agrupadas
        legend_title="Quarterbacks"
    )

    return fig

def stacked_bar(df,qb1,qb2):
    # Definir métricas de Air Yards
    air_yds_metrics = ["IAY/PA","CAY/Cmp","CAY/PA","YAC/Cmp"]
    formatted_metrics = ['Intended Air Yds/Att', 'Completed Air Yds/Cmp', 'Completed Air Yds/Att', 'Yds After Catch/Cmp']

    # Extraer datos de los dos QB seleccionados
    qb1_stats = df[df["Player"] == qb1][air_yds_metrics].values[0]
    qb2_stats = df[df["Player"] == qb2][air_yds_metrics].values[0]

    # Crear la gráfica de barras
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=formatted_metrics,
        y=qb1_stats,
        name=qb1,
        marker_color="red"
    ))

    fig.add_trace(go.Bar(
        x=formatted_metrics,
        y=qb2_stats,
        name=qb2,
        marker_color="blue"
    ))

    # Personalización del diseño
    fig.update_layout(
        title=f"Quarterback Passing Efficiency Metrics: {qb1} vs {qb2}",
        xaxis_title="Metrics",
        barmode="group",  # Barras agrupadas
        legend_title="Quarterbacks"
    )

    return fig

def plot_indicator_accuracy(data,qb,color,reference_value):
    rate = data['OnTgt%'].iloc[0]
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = rate,
        delta={'reference': (rate-reference_value)},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 100], 'color': 'black'},
                #{'range': [100, 158.3], 'color': 'black'}
            ],
            'threshold': {
                #'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))

    fig.update_layout(
        title=f"{qb} On-Target Throw Rate (No Spikes/Throwaways)",
        template="plotly_dark",
        width=400,  # Ajusta el ancho en píxeles
        height=400
    )

    return fig