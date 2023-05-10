import dash_bootstrap_components as dbc
import nltk
from dash import html, dcc
from bertopic import BERTopic
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
from markdown import markdown

nltk.download('stopwords')
german_stop_words = stopwords.words('german')
german_stop_words.extend(['ja', 'soweit', 'ganz', 'gibts', 'soweit', 'gerne', 'test', 'quiz'])
vectorizer_model = CountVectorizer(stop_words=german_stop_words)
topic_model = BERTopic(min_topic_size=6, language="multilingual", vectorizer_model=vectorizer_model)


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
        ((df_documents.intent == 'nlu_fallback') & (df_documents.timestamp < 1677063600))].index
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
    topics = topic_model.get_topics()
    graph = dcc.Graph(id='topic-graph', figure=topic_model.visualize_topics())
    graph_hierarchy = dcc.Graph(id='topic-hierarchy-graph', figure=topic_model.visualize_hierarchy())

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Topics Visualization", className="mb-1")]),
                dbc.CardBody([graph])]
                , style={"padding-bottom": "20px"}),
            dbc.Card([
                dbc.CardHeader([html.H5("Topics", className="mb-1")]),
                dbc.CardBody([graph_hierarchy])]
            ),
            dbc.Card([
                dbc.CardHeader([html.H5("Topics Hierarchy", className="mb-1")]),
                dbc.CardBody([graph_hierarchy])]
            )
        ], style={"padding-bottom": "20px"})
