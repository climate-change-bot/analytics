import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from wordcloud import WordCloud
from nltk.corpus import stopwords


def get_wordcloud(df_sentiment, title_header, graph_id):
    text = ' '.join(df_sentiment['text']).lower()

    wordcloud = WordCloud(
        stopwords=stopwords.words('german'),
        min_font_size=8,
        scale=2.5,
        background_color='#F9F9FA',
        collocations=True,
        min_word_length=4,
        collocation_threshold=3
    )

    wordcloud_image = wordcloud.generate(text)
    fig = go.Figure()
    fig.add_trace(go.Image(z=wordcloud_image))

    fig.update_xaxes(title=None)

    fig.update_layout(
        dragmode=None,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"t": 0, "b": 0, "l": 0, "r": 0},
        hovermode=False,
        paper_bgcolor="#F9F9FA",
        plot_bgcolor="#F9F9FA",
    )
    graph = dcc.Graph(id=graph_id, figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5(title_header, className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})


def get_wordclouds(df):
    df_negative_sentiment = df[(df.negative > 0.5) & (df.type_name == 'user')]
    df_positive_sentiment = df[(df.positive > 0.5) & (df.type_name == 'user')]

    return html.Div(
        [
            get_wordcloud(df_negative_sentiment, 'Words in Negative Sentiment', 'sentiment-wordcloud-negative-graph'),
            get_wordcloud(df_positive_sentiment, 'Words in Positive Sentiment', 'sentiment-wordcloud-positive-graph')

        ])
