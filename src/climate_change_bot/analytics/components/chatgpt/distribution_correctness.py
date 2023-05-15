import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from climate_change_bot.analytics.components.chatgpt.chatgpt import get_chatgpt_answers


def _count_all_containing_wrong(series):
    return ((series == 0) | (series == 1)).sum()


def _get_ratio(df):
    df_distribution = get_chatgpt_answers(df)
    df_distribution = df_distribution.groupby('sender_id')
    df_distribution = df_distribution.agg(
        total=('sender_id', 'count'),
        wrong=('chatgpt_correctness_of_content', _count_all_containing_wrong))

    df_distribution = df_distribution[df_distribution.wrong > 0]
    df_distribution['ratio'] = df_distribution['wrong'] / df_distribution['total']
    return df_distribution


def get_distribution_correctness(df):
    df_wrong = _get_ratio(df)

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(x=df_wrong['ratio'], marker_color='rgb(235, 52, 52)', nbinsx=60))

    fig.update_xaxes(title=None)
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title="Percentage of Conversation Length", fixedrange=True),
        yaxis=dict(title='Count', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph = dcc.Graph(id="graph-distribution", figure=fig)

    df_wrong['counts'] = df_wrong.groupby(['total', 'ratio'])['ratio'].transform('count')
    df_wrong['counts_scaled'] = df_wrong['counts'] * 5

    fig_2 = go.Figure()
    fig_2.add_trace(
        go.Scatter(x=df_wrong['total'], y=df_wrong['ratio'],
                   mode='markers',
                   marker=dict(
                       color='rgb(235, 52, 52)',
                       size=df_wrong['counts_scaled'],
                       sizemode='area',
                       sizeref=2. * max(df_wrong['counts_scaled']) / (40. ** 2),
                       sizemin=4
                   )))

    fig_2.update_xaxes(title=None)
    fig_2.update_layout(
        dragmode=None,
        xaxis=dict(title="Number of ChatGPT Messages per Conversation", fixedrange=True),
        yaxis=dict(title='Percentage of Incorrect Information', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph_2 = dcc.Graph(id="graph-length-vs-correctness", figure=fig_2)

    return html.Div([html.Div(
        [
            dbc.Card([
                dbc.CardHeader(
                    [html.H5(f"Distribution (Conversations with Wrong Content: {len(df_wrong)})", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"}),
        html.Div(
            [
                dbc.Card([
                    dbc.CardHeader(
                        [html.H5(f"Length vs Percentage of incorrect Information",
                                 className="mb-1")]),
                    dbc.CardBody([graph_2])]
                )
            ], style={"padding-bottom": "20px"})])
