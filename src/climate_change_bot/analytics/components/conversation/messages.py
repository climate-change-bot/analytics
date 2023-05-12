import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import datetime
import ast
import math

select_language_options = [{"label": "German", "value": 'de'},
                           {"label": "English", "value": "en"},
                           {"label": "French", "value": "fr"}]

select_is_climate_change_related_options = [{
    "label": html.Span(['Climate Change Related'], style={'color': 'green'}),
    "value": 1,
}, {
    "label": html.Span(['Not Climate Change Related'], style={'color': 'red'}),
    "value": 0,
}]

select_appropriate_options = [{
    "label": html.Span(['Correct in Context'], style={'color': 'green'}),
    "value": 1,
}, {
    "label": html.Span(['Wrong in Context'], style={'color': 'red'}),
    "value": 0,
}]

select_chatgpt_correctness_of_content_options = [{
    "label": html.Span(['Correct Content'], style={'color': 'green'}),
    "value": 2,
}, {
    "label": html.Span(['Partly Correct Content'], style={'color': '#DAA520'}),
    "value": 1,
}, {
    "label": html.Span(['Wrong Content'], style={'color': 'red'}),
    "value": 0,
}]

select_chatgpt_depth_options = [{
    "label": html.Span(['Detailed'], style={'color': 'green'}),
    "value": 2,
}, {
    "label": html.Span(['Medium depth'], style={'color': '#DAA520'}),
    "value": 1,
}, {
    "label": html.Span(['Superficial'], style={'color': 'red'}),
    "value": 0,
}]

select_sentiment_options = [{
    "label": html.Span(['Positive'], style={'color': 'green'}),
    "value": 2,
}, {
    "label": html.Span(['Neutral'], style={'color': 'gray'}),
    "value": 1,
}, {
    "label": html.Span(['Negative'], style={'color': 'red'}),
    "value": 0,
}]


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


def _get_sentiment_option(neutral, positive, negative):
    if positive > neutral and positive > negative:
        return 2
    elif neutral > positive and neutral > negative:
        return 1
    elif negative > positive and negative > neutral:
        return 0


def _display_sentiment(x):
    if x["type_name"] == "user" and not math.isnan(x['neutral']) and not math.isnan(x['positive']) and not math.isnan(
            x['negative']):
        return html.Div(
            [html.Hr(),
             dbc.Row([dbc.Col([html.Span(f"{x['neutral']:.2f} Neutral, ", style={'color': 'gray'}),
                               html.Span(f"{x['positive']:.2f} Positive, ", style={'color': 'green'}),
                               html.Span(f"{x['negative']:.2f} Negative", style={'color': 'red'})]),
                      dbc.Col(dcc.Dropdown(
                          options=select_sentiment_options,
                          value=_get_sentiment_option(x['neutral'], x['positive'], x['negative']),
                          id={'type': 'sentiment-select', 'index': x['index_message']},
                          clearable=False
                      ))])
             ])


def _display_user_commands(x):
    ignored_intents = ['greet', 'start_quiz', 'quiz_answer']
    if x["type_name"] == "user" and x["intent_name"] not in ignored_intents:
        return html.Div(
            [html.Hr(),
             dbc.Row([dbc.Col(dcc.Dropdown(
                 options=select_language_options,
                 value=x['language'],
                 id={'type': 'language-select', 'index': x['index_message']},
                 clearable=False
             )), dbc.Col(dcc.Dropdown(
                 options=select_is_climate_change_related_options,
                 value=x['is_climate_change_related'],
                 id={'type': 'climate-change-related-select', 'index': x['index_message']},
                 clearable=False
             ))])
             ])


def _display_bot_commands(x):
    ignored_intents = ['greet', 'start_quiz', 'quiz_answer']
    if x["type_name"] == "bot" and x["intent_name"] not in ignored_intents:
        return html.Div(
            [html.Hr(),
             dbc.Row([dbc.Col(dcc.Dropdown(
                 options=select_language_options,
                 value=x['language'],
                 id={'type': 'language-select', 'index': x['index_message']},
                 clearable=False
             )), dbc.Col(dcc.Dropdown(
                 options=select_is_climate_change_related_options,
                 value=x['is_climate_change_related'],
                 id={'type': 'climate-change-related-select', 'index': x['index_message']},
                 clearable=False
             )), dbc.Col(dcc.Dropdown(
                 options=select_appropriate_options,
                 value=x['appropriate_in_context_conversation'],
                 id={'type': 'appropriate-in-context-conversation-select', 'index': x['index_message']},
                 clearable=False
             )), dbc.Col(dcc.Dropdown(
                 options=select_chatgpt_correctness_of_content_options,
                 value=x['chatgpt_correctness_of_content'],
                 id={'type': 'chatgpt-correctness-of-content-select', 'index': x['index_message']},
                 clearable=False
             )) if x['is_chatgpt_answer'] == 1 else None, dbc.Col(dcc.Dropdown(
                 options=select_chatgpt_depth_options,
                 value=x['depth_chatgpt_answer'],
                 id={'type': 'chatgpt-depth-select', 'index': x['index_message']},
                 clearable=False
             )) if x['is_chatgpt_answer'] == 1 else None])
             ])


save_conversation_button = dbc.Button('Save Conversations', id='button-save-conversations', disabled=False)


def get_sidebar_conversation(df_conversation_messages):
    return html.Div([
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
        save_conversation_button,
        html.Hr()
    ])


delete_button = dbc.Button('Delete Conversation', color="danger")


def get_conversation_messages(df_conversation_messages):
    df_sentiment = df_conversation_messages.agg({'neutral': 'mean', 'negative': 'mean', 'positive': 'mean'})

    return html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.CardLink("Previous", href=f"{df_conversation_messages.iloc[0]['conversation_id'] - 1}"),
                        dbc.CardLink("Next", href=f"{df_conversation_messages.iloc[0]['conversation_id'] + 1}"),
                        html.Hr(),
                        html.Div(f"{df_sentiment['neutral']:.2f} Neutral", style={'color': 'gray'}),
                        html.Div(f"{df_sentiment['positive']:.2f} Positive", style={'color': 'green'}),
                        html.Div(f"{df_sentiment['negative']:.2f} Negative", style={'color': 'red'}),
                        html.Hr(),
                        dcc.ConfirmDialogProvider(
                            children=delete_button,
                            id='button-delete-conversation',
                            message='Are you sure you want to delete the conversation?'
                        ),
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
                    _display_sentiment(x[1]),
                    _display_user_commands(x[1]),
                    _display_bot_commands(x[1])
                ], color="primary" if x[1]["type_name"] == "user" else "secondary") for x in
                    df_conversation_messages.iterrows()]
            )]
    )
