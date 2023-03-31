import dash
from dash import html
import dash_bootstrap_components as dbc

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot import df

number_of_conversations = len(df['sender_id'].value_counts())

dash.register_page(__name__, path='/')

card = dbc.Card(
    dbc.CardBody(
        [
            html.H2("Conversations"),
            html.H3(number_of_conversations)
        ],
    ),
)

layout_content = [
    dbc.Row([dbc.Col(card)])
]

content = get_content(layout_content)
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])
