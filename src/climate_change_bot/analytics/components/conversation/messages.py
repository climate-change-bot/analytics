import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import datetime
import ast


def _get_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def _get_intents(intents):
    intents = ast.literal_eval(intents)
    return intents[1:]


def _display_intents(x):
    if x["type_name"] == "user":
        return html.P(" | ".join([f"intent: {y['name']}, confidence: {y['confidence']:.3f}" for y in
                                  _get_intents(x['intent_ranking']) if y['confidence'] > 0.05]),
                      className="mb-1")


def _display_user_commands(x):
    ignored_intents = ['greet', 'start_quiz', 'quiz_answer']
    if x["type_name"] == "user" and x["intent_name"] not in ignored_intents:
        select_options = [{"label": "German", "value": 'de'},
                          {"label": "English", "value": "en"},
                          {"label": "French", "value": "fr"}]

        return html.Div(
            [html.Hr(),
             dbc.Row([dbc.Col(dcc.Dropdown(
                 options=select_options,
                 value=x['language'],
                 id={'type': 'language-select', 'index': x['index_message']},
                 clearable=False
             ))])
             ])


def get_side_bar(df_conversation_messages):
    return [
        html.P(html.B(f"{df_conversation_messages.iloc[0]['sender_id']}")),
        html.P(
            f"Start: {_get_time(df_conversation_messages.iloc[0]['timestamp'])}"
        ),
        html.P(
            f"Chatbot Version: {df_conversation_messages.iloc[0]['chatbot_version']}"
        ),
        html.P(
            f"Rasa Version: {df_conversation_messages.iloc[0]['rasa_version']}"
        ),
        html.Hr(),
        dbc.Button('Save Conversations', id='button-save-conversations', disabled=False),
        html.Hr()
    ]


def get_conversation_messages(df_conversation_messages):
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.CardLink("Previous", href=f"{df_conversation_messages.iloc[0]['conversation_id'] - 1}"),
                        dbc.CardLink("Next", href=f"{df_conversation_messages.iloc[0]['conversation_id'] + 1}")
                    ]
                ),
                style={"width": "auto", "margin": "12px 0px"}
            ),
            dbc.ListGroup(
                [dbc.ListGroupItem([
                    html.Div(
                        [
                            html.Small(f"{_get_time(x[1]['timestamp'])}"),
                            html.H5(f"{x[1]['text']}", className="mb-1")
                        ]
                    ),
                    html.P(f"intent: {x[1]['intent']}, confidence: {x[1]['intent_confidence']:.3f}",
                           className="mb-1") if x[1]["type_name"] == "user" else None,
                    _display_intents(x[1]),
                    _display_user_commands(x[1])
                ], color="primary" if x[1]["type_name"] == "user" else "secondary") for x in
                    df_conversation_messages.iterrows()]
            )]
    )
