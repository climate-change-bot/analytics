import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd


def _get_durations(df):
    time_min_max = df.groupby('conversation_id')['timestamp_datetime'].agg(['min', 'max'])
    time_min_max['max'] = pd.to_datetime(time_min_max['max'])
    time_min_max['min'] = pd.to_datetime(time_min_max['min'])
    time_min_max['duration'] = time_min_max['max'] - time_min_max['min']
    time_min_max['duration_seconds'] = time_min_max['duration'].dt.total_seconds()
    # Longer conversations are like because they walked away from the computer
    time_min_max = time_min_max[time_min_max.duration_seconds < 3600]
    return time_min_max


def get_duration_whiskers(df_1, df_2, df_3):
    duration_1 = _get_durations(df_1)
    duration_2 = _get_durations(df_2)
    duration_3 = _get_durations(df_3)

    fig = go.Figure()
    fig.add_trace(go.Box(y=duration_1['duration_seconds'], name='Testphase 1', boxmean=True))
    fig.add_trace(go.Box(y=duration_2['duration_seconds'], name='Testphase 2', boxmean=True))
    fig.add_trace(go.Box(y=duration_3['duration_seconds'], name='Testphase 3', boxmean=True))
    fig.update_xaxes(title=None)
    fig.update_layout(
        showlegend=False,
        dragmode=None,
        yaxis=dict(title="Duration (s)", fixedrange=True),
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
