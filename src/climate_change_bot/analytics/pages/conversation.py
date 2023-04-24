import dash
from dash import html, callback, dcc
from dash.dependencies import Input, Output
import pandas as pd
import re

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.conversation.messages import get_side_bar, get_conversation_messages

dash.register_page(__name__, path_template="/conversation/<conversation_id>")


def layout(conversation_id=None):
    if conversation_id:
        content = get_content("conversation-content", [])
        sidebar = get_sidebar(html.Div(id="conversation-sidebar", children=[]))

        return html.Div(children=[
            dcc.Location(id='conversation-url', refresh=False), sidebar, content
        ])


@callback(
    Output('conversation-content', 'children'),
    Output('conversation-sidebar', 'children'),
    Input('global-data-not-filtered', 'data'),
    Input('conversation-url', 'pathname')
)
def update_conversation_content(data, pathname):
    df = pd.DataFrame(data)
    conversation_id = re.search(r'/conversation/(\w+)', pathname).group(1)
    if conversation_id and int(conversation_id) >= 0:
        df_conversation = df[df['conversation_id'] == int(conversation_id)]

        return get_conversation_messages(df_conversation), get_side_bar(df_conversation)
