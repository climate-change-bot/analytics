import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px


def get_sunburst_graph(df):
    chatgpt_index = df[
        (df.type_name == 'user') & (df.timestamp > 1677063600) & (df.intent_name == 'nlu_fallback')].index
    next_row_indices = [index + 1 for index in chatgpt_index]
    df_chatgpt_answer = df.iloc[next_row_indices]
    df_chatgpt_answer.reset_index(drop=True, inplace=True)

    df_chatgpt_answer['chatgpt_correctness_of_content'] = df_chatgpt_answer['chatgpt_correctness_of_content'].map(
        {0: 'Wrong', 1: 'Partly Correct', 2: 'Correct'})
    df_chatgpt_answer['depth_chatgpt_answer'] = df_chatgpt_answer['depth_chatgpt_answer'].map(
        {0: 'Superficial', 1: 'Medium depth', 2: 'Detailed'})
    color_discrete_map = {'Wrong': 'rgb(235, 52, 52)', 'Partly Correct': 'rgb(235, 214, 52)',
                          'Correct': 'rgb(46, 204, 113)'}

    fig = px.sunburst(df_chatgpt_answer, path=['chatgpt_correctness_of_content', 'depth_chatgpt_answer'],
                      color='chatgpt_correctness_of_content',
                      color_discrete_map=color_discrete_map)

    graph = dcc.Graph(id='sunburst-graph', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Correctness", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
