import dash
from dash import html
import dash_bootstrap_components as dbc

from climate_change_bot import df

dash.register_page(__name__, path='/')

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 56,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

card = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Sales"),
            html.H3("$104.2M")
        ],
    ),
)

card_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H1("Sales"),
            html.H3("$104.2M")
        ],
    ),
)

content = html.Div(id="page-content", style=CONTENT_STYLE, children=[
    dbc.Row([dbc.Col(card), dbc.Col(card_2)])
])

layout = html.Div(children=[
    sidebar, content
])
