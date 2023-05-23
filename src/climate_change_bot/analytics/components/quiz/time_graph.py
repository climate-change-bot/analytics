import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px


def get_quiz_time_graph(df):
    df_quiz = df[df.intent_name == 'start_quiz']
    daily_quiz = df_quiz.groupby('date').size().reset_index().rename(columns={0: 'quiz'})

    fig = px.bar(daily_quiz, x='date', y='quiz')
    fig.update_traces(marker_color='#228B22')
    fig.update_xaxes(title=None)
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title=None, fixedrange=True),
        yaxis=dict(title='Number of Quiz', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph = dcc.Graph(id='quiz-time-graph', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Quiz", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
