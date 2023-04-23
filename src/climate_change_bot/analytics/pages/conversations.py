import dash
from dash import html

from climate_change_bot.analytics.components.conversation.overview import get_conversations
from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot import df

dash.register_page(__name__, path='/conversations')

df_conversation_overview = df.groupby('sender_id')
df_conversation_overview = df_conversation_overview.agg(
    {'sender_id': 'size', 'neutral': 'mean', 'negative': 'mean', 'positive': 'mean', 'is_quiz': 'max',
     'timestamp': 'min', 'model_id': 'max', 'conversation_id': 'max'})
df_conversation_overview = df_conversation_overview.sort_values(by=['timestamp'], ascending=False)
df_conversation_overview = df_conversation_overview.rename(columns={'sender_id': 'number_of_chats'})

layout_content = [
    get_conversations(df_conversation_overview)
]

content = get_content(layout_content)
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])
