import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

from climate_change_bot.analytics.components.conversation.turn import get_turns


def get_turns_whiskers(df):
    number_of_turns, number_of_max_turns, turn_counts = get_turns(df)

    fig = go.Figure()
    fig.add_trace(go.Box(y=turn_counts, name='Turns', boxmean=True))
    fig.update_xaxes(title=None)
    fig.update_layout(
        dragmode=None,
        yaxis=dict(title="Number of Turns", fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph = dcc.Graph(id='whiskers-turns', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Turns", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
