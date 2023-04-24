import pandas as pd
import dash
from dash import html, callback
from dash.dependencies import Input, Output

from climate_change_bot.analytics.components.conversation.overview import get_conversations
from climate_change_bot.analytics.pages.base import get_content, get_sidebar

dash.register_page(__name__, path='/conversations')

content = get_content("conversations-content", [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('conversations-content', 'children'),
    [Input('global-data', 'data')]
)
def update_conversations(data):
    df = pd.DataFrame(data)
    df_conversation_overview = df.groupby('sender_id')
    df_conversation_overview = df_conversation_overview.agg(
        {'sender_id': 'size', 'neutral': 'mean', 'negative': 'mean', 'positive': 'mean', 'is_quiz': 'max',
         'timestamp': 'min', 'chatbot_version': 'max', 'rasa_version': 'max', 'conversation_id': 'max'})
    df_conversation_overview = df_conversation_overview.sort_values(by=['timestamp'], ascending=False)
    df_conversation_overview = df_conversation_overview.rename(columns={'sender_id': 'number_of_chats'})

    layout_content = [
        get_conversations(df_conversation_overview)
    ]
    return layout_content
