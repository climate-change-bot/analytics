import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import re

pattern = re.compile(r'/quiz_answer\{"(?P<key>[^"]+)":"(?P<value>true_[^"]+)"\}')


def _count_correct_answers(answers):
    correct_count = 0
    for answer in answers:
        if pattern.match(answer):
            correct_count += 1
    return correct_count


def _get_correct_answer_statistic(df_quiz_answers):
    results = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for conversation_id, group in df_quiz_answers.groupby('conversation_id'):
        group_size = len(group)
        for i in range(0, group_size, 8):
            if i + 8 > group_size:
                break
            answers = group['text'][i:i + 8]
            correct_count = _count_correct_answers(answers)
            results[correct_count] += 1

    return results


def get_number_of_correct_answer(df):
    df_quiz_answers = df[df.intent_name == 'quiz_answer']
    answer_counts = _get_correct_answer_statistic(df_quiz_answers)

    x = [str(key) for key in answer_counts.keys()]
    y = list(answer_counts.values())

    fig = go.Figure(
        data=[go.Bar(x=x, y=y)]
    )

    fig.update_layout(
        xaxis=dict(title="Number of correct answers per quiz", fixedrange=True),
        yaxis=dict(title="Frequency", fixedrange=True)
    )

    graph = dcc.Graph(id='quiz-answer-distribution-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Distribution of correct answers per quiz", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
