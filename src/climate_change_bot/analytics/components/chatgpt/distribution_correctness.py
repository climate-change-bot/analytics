import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from climate_change_bot.analytics.components.chatgpt.chatgpt import get_chatgpt_answers


def _count_partly_correct(series):
    return (series == 1).sum()


def _count_wrong(series):
    return (series == 0).sum()


def _get_card(df, count_function, color, title_x_axis, title_header, id):
    df_distribution = get_chatgpt_answers(df)
    df_distribution = df_distribution.groupby('sender_id')
    df_distribution = df_distribution.agg(
        total=('sender_id', 'count'),
        correct=('chatgpt_correctness_of_content', count_function))

    df_distribution = df_distribution[df_distribution.correct > 0]
    df_distribution['ratio'] = df_distribution['correct'] / df_distribution['total']

    fig = px.histogram(df_distribution, x="ratio", nbins=60, color_discrete_sequence=[color])
    fig.update_xaxes(title=None)
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title=title_x_axis, fixedrange=True),
        yaxis=dict(title='Count', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph = dcc.Graph(id=id, figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5(title_header, className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})


def get_distribution_correctness(df):
    return html.Div(
        [
            _get_card(df, _count_partly_correct, 'rgb(200, 180, 0)',
                      'Percentage of Partially Correct Answers in Conversation',
                      'Distribution Partly Correct Answers',
                      'histogram-partly-correct-graph'),
            _get_card(df, _count_wrong, 'rgb(235, 52, 52)',
                      'Percentage of Wrong Answers in Conversation',
                      'Distribution Wrong Answers',
                      'histogram-wrong-graph')
        ])
