import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import plotly.subplots as sp
import re
from climate_change_bot.analytics.components.quiz.quiz_text import questions, answers


def _add_description(question_statistic):
    question_statistic_text = {}
    for question in question_statistic.keys():
        question_text = questions[question]
        question_statistic_text[question_text] = {}
        for answer in question_statistic[question].keys():
            answer_text = answers[answer]
            question_statistic_text[question_text][answer_text] = question_statistic[question][answer]
    return question_statistic_text


def _get_question_statistic(df_quiz_answers):
    question_statistic = {}
    added_to_question = []
    pattern = r'/quiz_answer\{"(?P<key>[^"]+)":"(?P<value>[^"]+)"\}'
    for row in df_quiz_answers.to_dict('records'):
        match = re.search(pattern, row['text'])
        if match:
            key = match.group('key')
            value = match.group('value')
            if key not in question_statistic:
                question_statistic[key] = {}
            if f"{key}{row['conversation_id']}" not in added_to_question:
                if value not in question_statistic[key]:
                    question_statistic[key][value] = 1
                else:
                    question_statistic[key][value] += 1
                added_to_question.append(f"{key}{row['conversation_id']}")
        else:
            print(f"Could not correctly parse answer {row['text']}")

    sorted_question_statistic = {}

    for key, value_dict in question_statistic.items():
        sorted_value_dict = dict(
            sorted(value_dict.items(), key=lambda x: (x[0].startswith('true'), x[1]), reverse=True))
        sorted_question_statistic[key] = sorted_value_dict
    sorted_question_statistic = _add_description(sorted_question_statistic)
    return sorted_question_statistic


def get_answer_analysis(df):
    df_quiz_answers = df[df.intent_name == 'quiz_answer']
    answer_counts = _get_question_statistic(df_quiz_answers)

    questions = list(answer_counts.keys())

    fig = sp.make_subplots(rows=len(questions), cols=1, subplot_titles=questions)

    colors = ['#228B22', '#B22222', '#B22222', '#B22222']

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
                    name='Correct' if j == 0 else 'Wrong',
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
        yaxis=dict(title="Frequency", fixedrange=True)
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=True, gridcolor='rgba(180, 180, 180, 0.5)',
                     zerolinecolor='rgba(180, 180, 180, 0.5)')

    for ann in fig['layout']['annotations']:
        ann['font'] = dict(size=14, color='black')

    graph = dcc.Graph(id='quiz-detailed-answer-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Detailed Answer Analysis (First Attempt)", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
