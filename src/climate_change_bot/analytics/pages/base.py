import pandas as pd
from dash import html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 56,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
}

CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

filter_testphase = html.Div(
    [
        dbc.Label("Testphase:"),
        dbc.RadioItems(
            options=[
                {"label": "All", "value": 0},
                {"label": "1", "value": 1},
                {"label": "2", "value": 2},
                {"label": "3", "value": 3},
            ],
            value=0,
            id="filter-testphase",
            inline=True
        ),
        html.Hr()
    ]
)


def get_sidebar(nav_header=[], show_testphase=True):
    return html.Div(id="page-sidebar", children=[
        nav_header,
        filter_testphase if show_testphase else [],
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Conversations", href="/conversations", active="exact"),
                dbc.NavLink("Quiz", href="/quiz", active="exact"),
                dbc.NavLink("Intents", href="/intents", active="exact"),
                dbc.NavLink("Sentiment", href="/sentiment", active="exact"),
                dbc.NavLink("Topic", href="/topic", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ], style=SIDEBAR_STYLE)


def get_content(id_name, children):
    return html.Div(id=id_name, style=CONTENT_STYLE, children=children)


@callback(
    Output('global-data', 'data'),
    Input('filter-testphase', 'value'),
    State('global-data-not-filtered', 'data'),
)
def update_global_data(filter_value, data):
    df = pd.DataFrame(data)
    if filter_value == 0:
        return df.to_dict('records')
    else:
        df_filtered = df[df.testphase == filter_value]
        return df_filtered.to_dict('records')
