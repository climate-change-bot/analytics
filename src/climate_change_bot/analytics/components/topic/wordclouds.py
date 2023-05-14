from dash import html, dcc
from climate_change_bot.analytics.components.sentiment.wordclouds import get_wordcloud


def get_wordclouds(df):
    df_neutral_sentiment = df[(df.neutral > 0.5) & (df.type_name == 'user')]

    return html.Div(
        [
            get_wordcloud(df_neutral_sentiment, 'Most used Words', 'topic-wordcloud-graph')

        ])
