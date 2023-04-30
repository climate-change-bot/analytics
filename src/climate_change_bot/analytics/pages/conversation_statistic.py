import dash
from dash import html, callback
from dash.dependencies import Input, Output

from climate_change_bot.analytics.components.conversation.statistic.turns import get_turns_whiskers
from climate_change_bot.analytics.components.conversation.statistic.duration import get_duration_whiskers
from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.store import global_store

dash.register_page(__name__, path='/conversation-statistic')

content = get_content("conversation-statistic-content", [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('conversation-statistic-content', 'children'),
    [Input('signal-global-data', 'data')]
)
def update_conversation_statistic(data):
    df = global_store.get_data(data)

    layout_content = [
        get_turns_whiskers(df), get_duration_whiskers(df)
    ]
    return layout_content
