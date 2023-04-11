from dash import html
import dash_bootstrap_components as dbc

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


def get_sidebar(nav_header=[]):
    return html.Div(
        [
            nav_header,
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Conversations", href="/conversations", active="exact"),
                    dbc.NavLink("Quiz", href="/quiz", active="exact"),
                    dbc.NavLink("Intents", href="/intents", active="exact")
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )


def get_content(children):
    return html.Div(id="page-content", style=CONTENT_STYLE, children=children)
