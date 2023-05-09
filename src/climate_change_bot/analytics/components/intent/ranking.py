import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go


def get_ranking(df):
    df = df.sort_values(by=['conversation_id', 'timestamp']).reset_index()

    intents_index = df[
        (df.intent_name != 'nlu_fallback') & (df.intent_name != 'greet') & (df.type_name == 'user') & (
                df.intent_name != 'quiz_answer')].index
    next_row_indices = [index + 1 for index in intents_index]

    df_user_intents = df.iloc[intents_index]
    df_user_intents.reset_index(drop=True, inplace=True)
    df_bot_answer = df.iloc[next_row_indices]
    df_bot_answer.reset_index(drop=True, inplace=True)

    df_user_intents['appropriate_in_context_conversation'] = df_bot_answer['appropriate_in_context_conversation']

    grouped_df = df_user_intents.groupby(['intent_name', 'appropriate_in_context_conversation']).size().reset_index(
        name='count')

    pivot_df = grouped_df.pivot(index='intent_name', columns='appropriate_in_context_conversation', values='count')
    pivot_df = pivot_df.fillna(0)
    pivot_df['total'] = pivot_df[0] + pivot_df[1]
    pivot_df.sort_values(by='total', ascending=True, inplace=True)
    pivot_df.reset_index(inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=pivot_df['intent_name'],
        x=pivot_df[1],
        name='Correct',
        orientation='h',
        marker_color='blue'
    ))
    fig.add_trace(go.Bar(
        y=pivot_df['intent_name'],
        x=pivot_df[0],
        name='Wrong',
        orientation='h',
        marker_color='red'
    ))
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title="Counts", fixedrange=True),
        yaxis=dict(title='Intent Name', fixedrange=True),
        plot_bgcolor='white',
        bargap=0.5,
        font=dict(family='Arial', size=12, color='black'),
        height=700,
        barmode='stack'
    )
    graph = dcc.Graph(id='intent-ranking-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Ranking", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
