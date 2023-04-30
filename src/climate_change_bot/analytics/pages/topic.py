import dash
from dash import html, callback
from dash.dependencies import Input, Output

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.topic.berttopic import get_topic_graph
from climate_change_bot.analytics.store import global_store

dash.register_page(__name__, path='/topic')

content = get_content("topic-content", [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('topic-content', 'children'),
    Input('signal-global-data', 'data'),
    background=True,
)
def update_topic(data):
    df = global_store.get_data(data)

    layout_content = [
        get_topic_graph(df)
    ]
    return layout_content
