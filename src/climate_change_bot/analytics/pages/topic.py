import pandas as pd
import dash
from dash import html, callback
from dash.dependencies import Input, Output

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.topic.berttopic import get_topic_graph

dash.register_page(__name__, path='/topic')

content = get_content("topic-content", [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('topic-content', 'children'),
    [Input('global-data', 'data')],
    background=True,
)
def update_quiz(data):
    df = pd.DataFrame(data)

    layout_content = [
        get_topic_graph(df)
    ]
    return layout_content
