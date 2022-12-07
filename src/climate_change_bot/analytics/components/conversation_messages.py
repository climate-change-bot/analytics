import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime
import ast


def _get_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def _get_intents(intents):
    intents = ast.literal_eval(intents)
    return intents[1:]


def get_conversation_messages(df_conversation_messages):
    return html.Div(
        [
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
                    html.P(" | ".join([f"intent: {y['name']}, confidence: {y['confidence']:.3f}" for y in
                                       _get_intents(x[1]['intent_ranking']) if y['confidence'] > 0.05]),
                           className="mb-1")
                    if x[1]["type_name"] == "user" else None
                ], color="primary" if x[1]["type_name"] == "user" else "secondary") for x in
                    df_conversation_messages.iterrows()]
            )
        ]
    )
