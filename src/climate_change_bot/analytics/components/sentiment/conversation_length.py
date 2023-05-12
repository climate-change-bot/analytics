import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.subplots as sp
import plotly.graph_objects as go


def get_conversation_length_sentiment(df):
    df_conversation_overview = df[df.is_quiz == 0]
    df_conversation_overview = df_conversation_overview.groupby('sender_id')
    df_conversation_overview = df_conversation_overview.agg(
        {'sender_id': 'size', 'neutral': 'mean', 'negative': 'mean', 'positive': 'mean',
         'conversation_id': 'max'})
    df_conversation_overview = df_conversation_overview[df_conversation_overview.neutral.notnull() &
                                                        df_conversation_overview.negative.notnull() &
                                                        df_conversation_overview.positive.notnull()]

    fig = sp.make_subplots(rows=3, cols=1,
                           row_heights=[400, 400, 400],
                           vertical_spacing=0.15)
    fig.add_trace(
        go.Scatter(x=df_conversation_overview['sender_id'], y=df_conversation_overview['positive'], mode='markers',
                   name='Positive Sentiment', marker_color='green', marker_size=5), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=df_conversation_overview['sender_id'], y=df_conversation_overview['negative'], mode='markers',
                   name='Negative Sentiment', marker_color='red', marker_size=5), row=2, col=1)
    fig.add_trace(
        go.Scatter(x=df_conversation_overview['sender_id'], y=df_conversation_overview['neutral'], mode='markers',
                   name='Neutral Sentiment', marker_color='darkgray', marker_size=5), row=3, col=1)

    fig.update_layout(height=1200, width=1000)

    fig.update_xaxes(title_text="Number of Messages", row=1, col=1)
    fig.update_xaxes(title_text="Number of Messages", row=2, col=1)
    fig.update_xaxes(title_text="Number of Messages", row=3, col=1)
    fig.update_yaxes(title_text="Sentiment Score", row=1, col=1)
    fig.update_yaxes(title_text="Sentiment Score", row=2, col=1)
    fig.update_yaxes(title_text="Sentiment Score", row=3, col=1)

    graph = dcc.Graph(id='sentiment-length-conversation-graph', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Sentiment Analysis Conversation Length", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
