import dash
from dash import html, dcc, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from climate_change_bot.analytics.pages.base import get_content, get_sidebar

dash.register_page(__name__, path='/')


def get_turns(df_turns):
    df_turns = df_turns.sort_values(by=['sender_id', 'timestamp'])
    sender_id = 0
    previous_type = ''
    turns = 0
    turns_conversation = 0
    max_turns = 0
    for index, row in df_turns.iterrows():
        if row['sender_id'] != sender_id:
            sender_id = row['sender_id']
            previous_type = row['type_name']
            turns_conversation = 0
            # Don't count the welcome turns
            if turns > 0:
                turns -= 1
        if row['type_name'] == 'bot' and previous_type == 'user':
            turns += 1
            turns_conversation += 1
            if turns_conversation > max_turns:
                max_turns = turns_conversation
        previous_type = row['type_name']
    max_turns -= 1
    return turns, max_turns


content = get_content("home-content", [])
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])


@callback(
    Output('home-content', 'children'),
    Input('global-data', 'data'),
    background=True
)
def update_home(data):
    filtered_df = pd.DataFrame(data)
    number_of_quiz = len(filtered_df[filtered_df.intent_name == 'start_quiz'])

    number_of_conversations = len(filtered_df['sender_id'].value_counts())
    number_of_answers = len(filtered_df[filtered_df.type_name == 'bot'])
    number_of_max_answers = filtered_df[filtered_df.type_name == 'bot'].groupby('sender_id')['sender_id'].count().max()
    number_of_turns, number_of_max_turns = get_turns(filtered_df)

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

    daily_conversations = filtered_df.groupby(['date'])['sender_id'].nunique().reset_index().rename(
        columns={'sender_id': 'conversations'})

    fig = px.bar(daily_conversations, x='date', y='conversations')
    fig.update_xaxes(title=None)
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
