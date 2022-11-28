import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime


def _get_title(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def get_conversations(df_conversations):
    return html.Div(
        [
            dbc.ListGroup(
                [dbc.ListGroupItem(f"{_get_title(x[1]['timestamp'])} - {x[1]['number_of_chats']}",
                                   href=f"/conversations/{x[1]['sender_id']}") for x in
                 df_conversations.iterrows()]
            )
        ]
    )
