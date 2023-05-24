import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from climate_change_bot.analytics.store import TIME_CHAT_GPT_USED


def _get_counts(index, df):
    next_row_indices = [index + 1 for index in index]

    df_bot_answer = df.iloc[next_row_indices]
    df_bot_answer.reset_index(drop=True, inplace=True)

    grouped_df = df_bot_answer.groupby(['appropriate_in_context_conversation']).size().reset_index(name='count')
    total_appropriate = grouped_df.loc[grouped_df['appropriate_in_context_conversation'] == 1, 'count'].sum()
    total_inappropriate = grouped_df.loc[grouped_df['appropriate_in_context_conversation'] == 0, 'count'].sum()
    return total_appropriate, total_inappropriate


def get_intent_vs_chatgpt(df):
    intents_index = df[(df.type_name == 'user') & (df.intent_name != 'greet') & (df.intent_name != 'nlu_fallback') &
                       (df.intent_name != 'quiz_answer')].index
    total_appropriate, total_inappropriate = _get_counts(intents_index, df)

    chatgpt_index = df[
        (df.type_name == 'user') & (df.timestamp > TIME_CHAT_GPT_USED) & (df.intent_name == 'nlu_fallback')].index
    appropriate_chatgpt, not_appropriate_chatgpt = _get_counts(chatgpt_index, df)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Total Intents'],
        y=[total_appropriate],
        name='Correct in Context',
        marker_color='#228B22'
    ))

    fig.add_trace(go.Bar(
        x=['Total Intents'],
        y=[total_inappropriate],
        name='Incorrect in Context',
        marker_color='#B22222'
    ))

    fig.add_trace(go.Bar(
        x=['Total ChatGPT'],
        y=[appropriate_chatgpt],
        marker_color='#228B22',
        showlegend=False
    ))

    fig.add_trace(go.Bar(
        x=['Total ChatGPT'],
        y=[not_appropriate_chatgpt],
        marker_color='#B22222',
        showlegend=False
    ))

    fig.update_layout(
        dragmode=None,
        xaxis=dict(title="Counts", fixedrange=True),
        plot_bgcolor='white',
        bargap=0.5,
        font=dict(family='Arial', size=12, color='black'),
        height=700,
        barmode='stack'
    )
    graph = dcc.Graph(id='intent-vs-chatgpt-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Vs ChatGpt", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
