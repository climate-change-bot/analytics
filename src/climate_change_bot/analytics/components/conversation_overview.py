import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime
from climate_change_bot import get_version


def _get_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')


def _get_date(timestamp):
    return timestamp.strftime('%d.%m.%Y')


def _get_list_group(list_group_items):
    final_list_group_items = []
    time = datetime.max
    for list_group_item in list_group_items:
        next_time = datetime.fromtimestamp(list_group_item['timestamp'])
        if next_time.date() != time.date():
            time = next_time
            final_list_group_items.append(
                dbc.ListGroupItem([html.H5(f"{_get_date(time)}", className="mb-1")], color="primary"))
        final_list_group_items.append(
            dbc.ListGroupItem(
                f"{_get_time(list_group_item['timestamp'])} - messages: {list_group_item['number_of_chats']} - "
                f"chatbot_version: {get_version(list_group_item['model_id'])['chatbot_version']}",
                href=f"/conversations/{list_group_item['sender_id']}")
        )
    return final_list_group_items


def get_conversations(df_conversations):
    list_group_items = _get_list_group([x[1] for x in df_conversations.iterrows()])
    return html.Div(
        [
            dbc.ListGroup(list_group_items)
        ]
    )
