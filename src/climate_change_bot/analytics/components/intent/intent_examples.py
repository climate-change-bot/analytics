import dash_bootstrap_components as dbc
from dash import html
import re


def _get_number_of_added_examples(df_users, all_intents):
    added_examples = set()
    for row in df_users.to_dict('records'):
        if isinstance(row['text'], str):
            cleaned_input = row['text'].lower().strip()
            cleaned_input = re.sub(r'[\?!,.:]', '', cleaned_input)
            if cleaned_input in all_intents:
                added_examples.add(cleaned_input)

    return added_examples


def get_intent_examples(df, all_intents):
    all_examples = [element for x in all_intents if (sublist := x['examples']) for element in sublist]
    df_users = df[(df.type_name == 'user') & (df.intent_name != 'greet') & (df.intent_name != 'quiz_answer')]

    added_examples = _get_number_of_added_examples(df_users, all_examples)
    card = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Added Examples from User Inputs", style={'fontSize': 14}),
                html.H3(len(added_examples), className='text-center')
            ],
        ),
    )

    card_2 = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Number of Examples", style={'fontSize': 14}),
                html.H3(len(all_examples), className='text-center')
            ],
        ),
    )

    card_3 = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Number of Intents", style={'fontSize': 14}),
                html.H3(len(all_intents), className='text-center')
            ],
        ),
    )

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Counts", className="mb-1")]),
                dbc.CardBody(
                    [dbc.Row([dbc.Col(card), dbc.Col(card_2), dbc.Col(card_3)], style={'padding-bottom': 20})])]
            )
        ], style={"padding-bottom": "20px"})
