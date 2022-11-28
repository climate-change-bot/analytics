import dash
from dash import html

from climate_change_bot import df
from climate_change_bot.analytics.components.conversation_messages import get_conversation_messages

dash.register_page(__name__, path_template="/conversations/<sender_id>")


def layout(sender_id=None):
    df_conversation = df[df['sender_id'] == sender_id]

    return html.Div(children=[
        get_conversation_messages(df_conversation)
    ])
