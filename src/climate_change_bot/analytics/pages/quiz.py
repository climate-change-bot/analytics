import dash
from dash import html

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.quiz.time_graph import get_quiz_time_graph
from climate_change_bot import df

dash.register_page(__name__, path='/quiz')

layout_content = [
    get_quiz_time_graph(df)
]

content = get_content(layout_content)
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])
