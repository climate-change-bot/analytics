import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from climate_change_bot.analytics.components.chatgpt.chatgpt import get_chatgpt_answers


def get_sunburst_graph(df):
    df_chatgpt_answer = get_chatgpt_answers(df)

    df_chatgpt_answer['chatgpt_correctness_of_content'] = df_chatgpt_answer['chatgpt_correctness_of_content'].map(
        {0: 'Wrong', 1: 'Partly Correct', 2: 'Correct'})
    df_chatgpt_answer['depth_chatgpt_answer'] = df_chatgpt_answer['depth_chatgpt_answer'].map(
        {0: 'Superficial', 1: 'Medium Depth', 2: 'Detailed'})
    color_discrete_map = {'Wrong': 'rgb(235, 52, 52)', 'Partly Correct': 'rgb(235, 214, 52)',
                          'Correct': 'rgb(46, 204, 113)'}

    fig = px.sunburst(df_chatgpt_answer, path=['chatgpt_correctness_of_content', 'depth_chatgpt_answer'],
                      color='chatgpt_correctness_of_content',
                      color_discrete_map=color_discrete_map,
                      width=800, height=800)

    graph = dcc.Graph(id='sunburst-graph', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Correctness", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
