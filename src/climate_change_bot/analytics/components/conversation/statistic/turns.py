import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

from climate_change_bot.analytics.components.conversation.turn import get_turns


def get_turns_whiskers(df_1, df_2, df_3):
    number_of_turns, number_of_max_turns, turn_counts_1 = get_turns(df_1)
    number_of_turns, number_of_max_turns, turn_counts_2 = get_turns(df_2)
    number_of_turns, number_of_max_turns, turn_counts_3 = get_turns(df_3)

    fig = go.Figure()
    fig.add_trace(go.Box(y=turn_counts_1, name='Testphase 1', boxmean=True))
    fig.add_trace(go.Box(y=turn_counts_2, name='Testphase 2', boxmean=True))
    fig.add_trace(go.Box(y=turn_counts_3, name='Testphase 3', boxmean=True))
    fig.update_xaxes(title=None)
    fig.update_layout(
        showlegend=False,
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
