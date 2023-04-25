import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import plotly.subplots as sp
import re


def get_question_statistic(df_quiz_answers):
    question_statistic = {}
    pattern = r'/quiz_answer\{"(?P<key>[^"]+)":"(?P<value>[^"]+)"\}'
    for row in df_quiz_answers.to_dict('records'):
        match = re.search(pattern, row['text'])
        if match:
            key = match.group('key')
            value = match.group('value')
            if key not in question_statistic:
                question_statistic[key] = {}

            if value not in question_statistic[key]:
                question_statistic[key][value] = 1
            else:
                question_statistic[key][value] += 1
        else:
            print(f"Could not correctly parse answer {row['text']}")

    sorted_question_statistc = {}

    for key, value_dict in question_statistic.items():
        sorted_value_dict = dict(
            sorted(value_dict.items(), key=lambda x: (x[0].startswith('true'), x[1]), reverse=True))
        sorted_question_statistc[key] = sorted_value_dict
    return sorted_question_statistc


def get_answer_analysis(df):
    df_quiz_answers = df[df.intent_name == 'quiz_answer']
    answer_counts = get_question_statistic(df_quiz_answers)

    questions = list(answer_counts.keys())

    fig = sp.make_subplots(rows=len(questions), cols=1, subplot_titles=questions)

    colors = ['#636EFA', '#EF553B', '#EF553B', '#EF553B']

    for i, (question, counts) in enumerate(answer_counts.items()):
        answers, counts = zip(*counts.items())
        bar_colors = colors[: len(answers)]

        for j, (answer, count, color) in enumerate(zip(answers, counts, bar_colors)):
            fig.add_trace(
                go.Bar(
                    x=[answer],
                    y=[count],
                    marker_color=color,
                    text=count,
                    textposition='auto',
                    name='Richtig' if j == 0 else 'Falsch',
                    legendgroup="group{}".format(j),
                    showlegend=True if (i == 0 and j < 2) else False
                ),
                row=i + 1,
                col=1,
            )

    fig.update_layout(
        height=300 * len(questions),
        plot_bgcolor='rgba(255, 255, 255, 1)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        margin=dict(t=50, b=10),
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=True, gridcolor='rgba(180, 180, 180, 0.5)',
                     zerolinecolor='rgba(180, 180, 180, 0.5)')

    for ann in fig['layout']['annotations']:
        ann['font'] = dict(size=14, color='black')

    graph = dcc.Graph(id='intent-ranking-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Quiz Analysis", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
