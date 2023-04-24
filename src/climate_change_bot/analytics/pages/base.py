from dash import html
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


def get_sidebar(nav_header=[]):
    return html.Div(id="page-sidebar", children=[
        nav_header,
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Conversations", href="/conversations", active="exact"),
                dbc.NavLink("Quiz", href="/quiz", active="exact"),
                dbc.NavLink("Intents", href="/intents", active="exact"),
                dbc.NavLink("Topic", href="/topic", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ], style=SIDEBAR_STYLE)


def get_content(id_name, children):
    return html.Div(id=id_name, style=CONTENT_STYLE, children=children)
