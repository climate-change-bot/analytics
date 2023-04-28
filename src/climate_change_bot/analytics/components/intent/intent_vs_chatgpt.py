import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go


def get_intent_vs_chatgpt(df):
    df_intents = df[(df.type_name == 'user') & (df.intent_name != 'greet') & (df.intent_name != 'nlu_fallback') &
                    (df.intent_name != 'quiz_answer')]
    df_chatgpt = df[(df.type_name == 'user') & (df.timestamp > 1677063600) & (df.intent_name == 'nlu_fallback')]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=['Intents'], y=[len(df_intents)], name='intents'))
    fig.add_trace(go.Bar(x=['ChatGPT'], y=[len(df_chatgpt)], name='chatgpt'))

    fig.update_layout(
        dragmode=None,
        xaxis=dict(title="Counts", fixedrange=True),
        plot_bgcolor='white',
        bargap=0.5,
        font=dict(family='Arial', size=12, color='black'),
        height=700
    )
    graph = dcc.Graph(id='intent-vs-chatgpt-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Vs ChatGpt", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
