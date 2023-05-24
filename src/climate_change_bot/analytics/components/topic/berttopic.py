import dash_bootstrap_components as dbc
import nltk
from dash import html, dcc
from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
from markdown import markdown
from climate_change_bot.analytics.store import TIME_CHAT_GPT_USED

nltk.download('stopwords')
german_stop_words = stopwords.words('german')
german_stop_words.extend(
    ['ja', 'soweit', 'ganz', 'gibts', 'soweit', 'gerne', 'test', 'quiz', 'c02', 'dmo', '2016', '20', 'bilder',
     'zurück', 'daher', 'weiterhin'])
vectorizer_model = CountVectorizer(stop_words=german_stop_words)
np.random.seed(42)  # To get allways the same result.
representation_model = MaximalMarginalRelevance(diversity=0.2)
topic_model = BERTopic(min_topic_size=6, language="multilingual", vectorizer_model=vectorizer_model,
                       representation_model=representation_model)


def _filter_text(text):
    return not text.startswith('Willkommen') and not text.startswith('Herzlich Willkommen')


def _clean_text(text):
    html = markdown(text)
    return BeautifulSoup(html, features="html.parser").get_text()


def _filter_next_row(df, condition_indices):
    next_row_indices = [index + 1 for index in condition_indices]
    return df.drop(next_row_indices, errors='ignore')


def _get_conversations_as_string(df):
    df_documents = df.sort_values(by=['conversation_id', 'timestamp'])

    # Filter greet messages
    condition_indices = df_documents[df_documents.text == '/greet'].index
    df_documents = _filter_next_row(df_documents, condition_indices)

    # Filter fallback messages before using chatgpt
    condition_indices = df_documents[
        ((df_documents.intent == 'nlu_fallback') & (df_documents.timestamp < TIME_CHAT_GPT_USED))].index
    df_documents = _filter_next_row(df_documents, condition_indices)

    # Apply all other filters
    df_documents = df_documents[(df_documents.text != '/greet') & (df_documents.is_quiz == 0) &
                                (df_documents.is_climate_change_related == 1) & (df_documents.language == 'de')]
    df_documents = df_documents[((df.intent == 'nlu_fallback') & (df.is_chatgpt_answer == 0))]
    df_documents = df_documents[
        df_documents['text'].apply(lambda x: isinstance(x, str) and _filter_text(x))]
    df_documents = df_documents.groupby('conversation_id')['text'].agg(lambda x: ' '.join(x)).reset_index()
    conversations = df_documents['text'].tolist()
    return [_clean_text(conversation) for conversation in conversations]


def get_topic_graph(df):
    conversations = _get_conversations_as_string(df)
    topic_model.fit_transform(conversations)
    graph = dcc.Graph(id='topic-graph', figure=topic_model.visualize_topics())
    graph_bar = dcc.Graph(id='topic-bar-graph', figure=topic_model.visualize_barchart(top_n_topics=20, title=""))

    return html.Div(
        [
            html.Div(
                [
                    dbc.Card([
                        dbc.CardHeader([html.H5("Topics Map", className="mb-1")]),
                        dbc.CardBody([graph])])
                ], style={"padding-bottom": "20px"}),
            html.Div(
                [
                    dbc.Card([
                        dbc.CardHeader([html.H5("Topics", className="mb-1")]),
                        dbc.CardBody([graph_bar])])
                ], style={"padding-bottom": "20px"})
        ], style={"padding-bottom": "20px"})
