import dash
from dash import html, dcc, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.conversation.turn import get_turns
from climate_change_bot.analytics.store import global_store

dash.register_page(__name__, path='/')

content = get_content("home-content", [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


def _get_number_of_quiz(df):
    df_quiz_answers = df[df.intent_name == 'quiz_answer']
    count = 0
    for conversation_id, group in df_quiz_answers.groupby('sender_id'):
        group_size = len(group)
        if group_size >= 8:
            count += int(group_size / 8)
    return count


@callback(
    Output('home-content', 'children'),
    Input('signal-global-data', 'data'),
    background=True
)
def update_home(value):
    df = global_store.get_data(value)
    number_of_quiz = _get_number_of_quiz(df)

    number_of_conversations = len(df['sender_id'].value_counts())
    number_of_answers = len(df[df.type_name == 'bot'])
    number_of_max_answers = df[df.type_name == 'bot'].groupby('sender_id')['sender_id'].count().max()
    number_of_turns, number_of_max_turns, turn_counts = get_turns(df)

    card = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Quiz", style={'fontSize': 14}),
                html.H3(number_of_quiz, className='text-center')
            ],
        ),
    )

    card_2 = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Conversations", style={'fontSize': 14}),
                html.H3(number_of_conversations, className='text-center')
            ],
        ),
    )

    card_3 = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Answers", style={'fontSize': 14}),
                html.H3(number_of_answers, className='text-center'),
                html.Div(f"Max: {number_of_max_answers}", className='text-center', style={'fontSize': 14}),
                html.Div(f"Avg: {(number_of_answers / number_of_conversations):.2f}", className='text-center',
                         style={'fontSize': 14})

            ],
        ),
    )

    card_4 = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Turns", style={'fontSize': 14}),
                html.H3(number_of_turns, className='text-center'),
                html.Div(f"Max: {number_of_max_turns}", className='text-center', style={'fontSize': 14}),
                html.Div(f"Avg: {(number_of_turns / number_of_conversations):.2f}", className='text-center',
                         style={'fontSize': 14})
            ],
        ),
    )

    daily_conversations = df.groupby(['date'])['sender_id'].nunique().reset_index().rename(
        columns={'sender_id': 'conversations'})

    fig = px.bar(daily_conversations, x='date', y='conversations')
    fig.update_xaxes(title=None)
    fig.update_traces(marker_color='#228B22')
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title=None, fixedrange=True),
        yaxis=dict(title='Number of Conversations', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )

    layout_content = [
        dbc.Row([dbc.Col(card), dbc.Col(card_2), dbc.Col(card_3), dbc.Col(card_4)], style={'padding-bottom': 20}),
        dbc.Row([dbc.Card(dbc.CardBody(dcc.Graph(figure=fig)))], style={'padding-left': 11, 'padding-right': 11})
    ]

    return layout_content
