import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go


def get_total_graph(df):
    df_sentiment = df[df.neutral.notnull() & df.negative.notnull() & df.positive.notnull()]
    df_sentiment = df_sentiment.agg({'neutral': 'mean', 'negative': 'mean', 'positive': 'mean'})

    fig = go.Figure()

    fig.add_trace(go.Bar(x=['Neutral'], y=[df_sentiment['neutral']], name='Neutral', marker_color='gray'))
    fig.add_trace(go.Bar(x=['Negativ'], y=[df_sentiment['negative']], name='Negativ', marker_color='red'))
    fig.add_trace(go.Bar(x=['Positiv'], y=[df_sentiment['positive']], name='Positiv', marker_color='green'))

    fig.update_xaxes(title=None)
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title=None, fixedrange=True),
        yaxis=dict(title='Average Sentiment', fixedrange=True),
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black')
    )

    graph = dcc.Graph(id='sentiment-total-graph', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Average Sentiment", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
