import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime


def _get_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def get_conversation_messages(df_conversation_messages):
    return html.Div(
        [
            dbc.ListGroup(
                [dbc.ListGroupItem(f"{_get_time(x[1]['timestamp'])} - {x[1]['text']}",
                                   ) for x in
                 df_conversation_messages.iterrows()]
            )
        ]
    )
