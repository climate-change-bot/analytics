import pandas as pd
import dash
from dash import html, callback
from dash.dependencies import Input, Output

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.sentiment.stacked_area_graph import get_time_graph
from climate_change_bot.analytics.components.sentiment.total_graph import get_total_graph

dash.register_page(__name__, path='/sentiment')

content = get_content('sentiment-content', [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('sentiment-content', 'children'),
    [Input('global-data', 'data')],
    background=True,
)
def update_quiz(data):
    df = pd.DataFrame(data)

    layout_content = [
        get_time_graph(df), get_total_graph(df)
    ]
    return layout_content
