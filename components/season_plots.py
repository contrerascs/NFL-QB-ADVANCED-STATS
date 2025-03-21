import plotly.graph_objects as go

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