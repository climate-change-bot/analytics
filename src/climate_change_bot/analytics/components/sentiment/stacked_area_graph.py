import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go


def get_time_graph(df):
    df_sentiment = df[df.neutral.notnull() & df.negative.notnull() & df.positive.notnull()]

    df_sentiment = df_sentiment.groupby('date').agg({'neutral': 'mean', 'negative': 'mean', 'positive': 'mean'})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(df_sentiment.index), y=df_sentiment['positive'], name='Positiv', stackgroup='one',
                             fill='tonexty', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=list(df_sentiment.index), y=df_sentiment['neutral'], name='Neutral', stackgroup='one',
                             fill='tonexty', line=dict(color='gray')))
    fig.add_trace(go.Scatter(x=list(df_sentiment.index), y=df_sentiment['negative'], name='Negativ', stackgroup='one',
                             fill='tonexty', line=dict(color='red')))

    fig.update_xaxes(title=None)

    fig.update_layout(
        dragmode=None,
        xaxis=dict(title=None, fixedrange=True),
        yaxis=dict(title='Sentiment Value', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )
    graph = dcc.Graph(id='sentiment-time-graph', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Sentiment over Time", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
