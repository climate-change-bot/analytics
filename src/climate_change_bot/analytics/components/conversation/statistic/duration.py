import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

from climate_change_bot.analytics.components.conversation.turn import get_turns


def get_duration_whiskers(df):
    time_min_max = df.groupby('conversation_id')['timestamp_datetime'].agg(['min', 'max'])
    time_min_max['max'] = pd.to_datetime(time_min_max['max'])
    time_min_max['min'] = pd.to_datetime(time_min_max['min'])
    time_min_max['duration'] = time_min_max['max'] - time_min_max['min']
    time_min_max['duration_seconds'] = time_min_max['duration'].dt.total_seconds()
    # Longer conversations are like because they walked away from the computer
    time_min_max = time_min_max[time_min_max.duration_seconds < 3600]

    fig = go.Figure()
    fig.add_trace(go.Box(y=time_min_max['duration_seconds'], name='Durations', boxmean=True))
    fig.update_xaxes(title=None)
    fig.update_layout(
        dragmode=None,
        yaxis=dict(title="Duration", fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph = dcc.Graph(id='whiskers-duration', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Conversation Duration", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
