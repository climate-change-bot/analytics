import dash
from dash import html

from climate_change_bot import df
from climate_change_bot.analytics.components.conversation_messages import get_conversation_messages

dash.register_page(__name__, path_template="/conversations/<conversation_id>")


def layout(conversation_id=None):
    df_conversation = df[df['conversation_id'] == int(conversation_id)]

    return html.Div(children=[
        get_conversation_messages(df_conversation)
    ])
