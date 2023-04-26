import dash
import dash_bootstrap_components as dbc
from dash import html, callback, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import re
import os

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.conversation.messages import get_side_bar, get_conversation_messages

dash.register_page(__name__, path_template="/conversation/<conversation_id>")
file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')


def layout(conversation_id=None):
    if conversation_id:
        content = get_content("conversation-content", [])
        sidebar = get_sidebar(html.Div(id="conversation-sidebar", children=[
        ]), show_testphase=False)

        return html.Div(children=[
            dcc.Location(id='conversation-url', refresh=False), sidebar, content, html.Div(id='output')
        ])


@callback(
    Output('conversation-content', 'children'),
    Output('conversation-sidebar', 'children'),
    Input('global-data-not-filtered', 'data'),
    Input('conversation-url', 'pathname')
)
def update_conversation_content(data, pathname):
    df = pd.DataFrame(data)
    if isinstance(pathname, str):
        conversation_id = re.search(r'/conversation/(\w+)', pathname).group(1)
        if conversation_id and int(conversation_id) >= 0:
            df_conversation = df[df['conversation_id'] == int(conversation_id)]
            if len(df_conversation):
                return get_conversation_messages(df_conversation), get_side_bar(df_conversation)
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


def _set_value(data, column):
    triggered = callback_context.triggered
    df = pd.DataFrame(data)
    if len(triggered) == 1:
        index = _extract_index(triggered[0]['prop_id'])
        if index:
            value = triggered[0]['value']
            df.loc[df.index_message == index, column] = value
    return df.to_dict('records')


@callback(
    Output('global-data-not-filtered', 'data', allow_duplicate=True),
    Input({'type': 'language-select', 'index': ALL}, 'value'),
    State('global-data-not-filtered', 'data'),
    prevent_initial_call=True
)
def language_select_change(value, data):
    return _set_value(data, 'language')


@callback(
    Output('global-data-not-filtered', 'data', allow_duplicate=True),
    Input({'type': 'climate-change-related-select', 'index': ALL}, 'value'),
    State('global-data-not-filtered', 'data'),
    prevent_initial_call=True
)
def language_select_change(value, data):
    return _set_value(data, 'is_climate_change_related')


@callback(
    Output('global-data-not-filtered', 'data', allow_duplicate=True),
    Input({'type': 'appropriate-in-context-conversation-select', 'index': ALL}, 'value'),
    State('global-data-not-filtered', 'data'),
    prevent_initial_call=True
)
def language_select_change(value, data):
    return _set_value(data, 'appropriate_in_context_conversation')


@callback(
    Output('global-data-not-filtered', 'data', allow_duplicate=True),
    Input({'type': 'chatgpt-correctness-of-content-select', 'index': ALL}, 'value'),
    State('global-data-not-filtered', 'data'),
    prevent_initial_call=True
)
def language_select_change(value, data):
    return _set_value(data, 'chatgpt_correctness_of_content')


@callback(
    Output('output', 'children'),
    Input('button-save-conversations', 'n_clicks'),
    State('global-data-not-filtered', 'data'),
    background=True,
    prevent_initial_call=True,
    running=[
        (Output("button-save-conversations", "disabled"), True, False),
    ],
)
def save_conversations(n_clicks, data):
    if n_clicks:
        df = pd.DataFrame(data)
        with pd.ExcelWriter(file_name, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name='conversations')

    return html.Div()


@callback(
    Output('global-data-not-filtered', 'data', allow_duplicate=True),
    Input('button-delete-conversation', 'submit_n_clicks'),
    State('global-data-not-filtered', 'data'),
    State('conversation-url', 'pathname'),
    background=True,
    prevent_initial_call=True
)
def delete_conversation(submit_n_clicks, data, pathname):
    df = pd.DataFrame(data)
    if submit_n_clicks:
        conversation_id = re.search(r'/conversation/(\w+)', pathname).group(1)
        if conversation_id and int(conversation_id) >= 0:
            df = df[df['conversation_id'] != int(conversation_id)]
    return df.to_dict('records')
