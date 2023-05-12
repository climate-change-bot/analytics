import dash
import dash_bootstrap_components as dbc
from dash import html, callback, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import re
import os

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.conversation.messages import get_sidebar_conversation, \
    get_conversation_messages
from climate_change_bot.analytics.store import global_store

dash.register_page(__name__, path_template="/conversation/<conversation_id>")
file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')


def layout(conversation_id=None):
    if conversation_id:
        content, sidebar = get_conversation_content(conversation_id)
        content = get_content('conversation-content', content)
        return html.Div(children=[
            dcc.Location(id='conversation-url', refresh=False), sidebar, content,
            html.Div(id='output', style={'display': 'none'})
        ])


def get_conversation_content(conversation_id):
    if conversation_id and int(conversation_id) >= 0:
        df = global_store.get_data(0)
        df_conversation = df[df['conversation_id'] == int(conversation_id)]
        if len(df_conversation):
            return get_conversation_messages(df_conversation), \
                get_sidebar(get_sidebar_conversation(df_conversation), show_testphase=False)
        else:
            return html.Div([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(f"The conversation id {conversation_id} does not exist"),
                            dbc.CardLink("Previous", href=f"{int(conversation_id) - 1}"),
                            dbc.CardLink("Next", href=f"{int(conversation_id) + 1}")
                        ]
                    ),
                    style={"width": "auto", "margin": "12px 0px"}
                )
            ]), []


def _extract_index(index):
    pattern = r'"index":(\d+)'
    match = re.search(pattern, index)
    if match:
        return int(match.group(1))


def _set_value(column):
    triggered = callback_context.triggered
    if len(triggered) == 1:
        df = global_store.get_data(0)
        index = _extract_index(triggered[0]['prop_id'])
        if index:
            value = triggered[0]['value']
            df.loc[df.index_message == index, column] = value
    return html.Div()


@callback(
    Output('output', 'children', allow_duplicate=True),
    Input({'type': 'language-select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def language_select_change(value):
    return _set_value('language')


@callback(
    Output('output', 'children', allow_duplicate=True),
    Input({'type': 'climate-change-related-select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def language_select_change(value):
    return _set_value('is_climate_change_related')


@callback(
    Output('output', 'children', allow_duplicate=True),
    Input({'type': 'appropriate-in-context-conversation-select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def language_select_change(value):
    return _set_value('appropriate_in_context_conversation')


@callback(
    Output('output', 'children', allow_duplicate=True),
    Input({'type': 'chatgpt-correctness-of-content-select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def language_select_change(value):
    return _set_value('chatgpt_correctness_of_content')


@callback(
    Output('output', 'children', allow_duplicate=True),
    Input({'type': 'chatgpt-depth-select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def language_select_change(value):
    return _set_value('depth_chatgpt_answer')


@callback(
    Output('output', 'children', allow_duplicate=True),
    Input({'type': 'sentiment-select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def sentiment_change(value):
    triggered = callback_context.triggered
    if len(triggered) == 1:
        df = global_store.get_data(0)
        index = _extract_index(triggered[0]['prop_id'])
        if index:
            value = triggered[0]['value']
            if value == 2:
                df.loc[df.index_message == index, 'positive'] = 1.0
                df.loc[df.index_message == index, 'negative'] = 0.0
                df.loc[df.index_message == index, 'neutral'] = 0.0
            elif value == 1:
                df.loc[df.index_message == index, 'positive'] = 0.0
                df.loc[df.index_message == index, 'negative'] = 0.0
                df.loc[df.index_message == index, 'neutral'] = 1.0
            elif value == 0:
                df.loc[df.index_message == index, 'positive'] = 0.0
                df.loc[df.index_message == index, 'negative'] = 1.0
                df.loc[df.index_message == index, 'neutral'] = 0.0
            else:
                print('could not update sentiment')
    return html.Div()


@callback(
    Output('output', 'children'),
    Input('button-save-conversations', 'n_clicks'),
    prevent_initial_call=True,
    running=[
        (Output("button-save-conversations", "disabled"), True, False),
    ],
)
def save_conversations(n_clicks):
    if n_clicks:
        df = global_store.get_data(0)
        with pd.ExcelWriter(file_name, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name='conversations', index=False)
            print("conversation saved")

    return html.Div()


@callback(
    Output('conversation-url', 'pathname'),
    Input('button-delete-conversation', 'submit_n_clicks'),
    State('conversation-url', 'pathname'),
    prevent_initial_call=True
)
def delete_conversation(submit_n_clicks, pathname):
    if submit_n_clicks:
        conversation_id = re.search(r'/conversation/(\w+)', pathname).group(1)
        if conversation_id and int(conversation_id) >= 0:
            df = global_store.get_data(0)
            df = df[df['conversation_id'] != int(conversation_id)]
            global_store.set_data(df)
            print("conversation deleted")
    return pathname
