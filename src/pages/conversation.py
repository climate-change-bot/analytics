import dash
from dash import html

from src import df
from src.components.conversation_messages import get_conversation_messages

dash.register_page(__name__, path_template="/conversations/<sender_id>")


def layout(sender_id=None):
    df_conversation = df[df['sender_id'] == sender_id]

    return html.Div(children=[
        get_conversation_messages(df_conversation)
    ])
