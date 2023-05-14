import dash
from dash import html, callback
from dash.dependencies import Input, Output

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.chatgpt.sunburst_graph import get_sunburst_graph
from climate_change_bot.analytics.components.chatgpt.distribution_correctness import get_distribution_correctness
from climate_change_bot.analytics.store import global_store

dash.register_page(__name__, path='/chatgpt')

content = get_content('chatgpt-content', [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('chatgpt-content', 'children'),
    Input('signal-global-data', 'data'),
    background=True,
)
def update_sentiment(data):
    df = global_store.get_data(data)

    layout_content = [
        get_sunburst_graph(df), get_distribution_correctness(df)
    ]
    return layout_content
