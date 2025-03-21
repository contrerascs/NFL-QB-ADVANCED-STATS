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

def plot_radar_chart(df, qb1, qb2, season):
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
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title=f'Comparación de {qb1} vs {qb2} en {season}',
        template='plotly_dark'
    )
    
    return fig