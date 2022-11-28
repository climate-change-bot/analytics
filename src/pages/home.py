import dash
from dash import html

from src.components.conversation_overview import get_conversations
from src import df

dash.register_page(__name__, path='/')

df_conversation_overview = df.drop_duplicates(subset=['sender_id'])
df_conversation_overview = df_conversation_overview.sort_values(by=['timestamp'], ascending=False)

layout = html.Div(children=[
       get_conversations(df_conversation_overview)
])
