import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime
import math


def _get_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')


def _get_date(timestamp):
    return timestamp.strftime('%d.%m.%Y')


def _get_list_item_color(positive, negative, neutral):
    if not math.isnan(positive) and not math.isnan(neutral) and not math.isnan(negative):
        if positive > negative and positive > neutral:
            return "success"
        elif negative > positive and negative > neutral:
            return "danger"
        elif neutral > positive and neutral > negative:
            return "secondary"
    return "white"


def _get_list_group(list_group_items):
    final_list_group_items = []
    time = datetime.max
    for list_group_item in list_group_items:
        next_time = datetime.fromtimestamp(list_group_item['timestamp'])
        list_item_color = _get_list_item_color(list_group_item['positive'], list_group_item['negative'],
                                               list_group_item['neutral'])
        if next_time.date() != time.date():
            time = next_time
            final_list_group_items.append(
                dbc.ListGroupItem([html.H5(f"{_get_date(time)}", className="mb-1")], color="primary"))
        final_list_group_items.append(
            dbc.ListGroupItem(
                f"{_get_time(list_group_item['timestamp'])} - has quiz: {list_group_item['is_quiz']} - "
                f"messages: {list_group_item['number_of_chats']} - "
                f"chatbot version: {list_group_item['chatbot_version']}",
                href=f"/conversation/{list_group_item['conversation_id']}",
                color=list_item_color)
        )
    return final_list_group_items


def get_conversations(df_conversations):
    list_group_items = _get_list_group([x[1] for x in df_conversations.iterrows()])
    return html.Div(
        [
            dbc.ListGroup(list_group_items)
        ]
    )
