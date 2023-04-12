import dash_bootstrap_components as dbc
from dash import html, dcc
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bs4 import BeautifulSoup
from markdown import markdown

ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
topic_model = BERTopic(min_topic_size=3, language="multilingual", ctfidf_model=ctfidf_model)


def _filter_text(text):
    return not text.startswith('Willkommen') and not text.startswith('Herzlich Willkommen')


def _clean_text(text):
    html = markdown(text)
    return BeautifulSoup(html, features="html.parser").get_text()


def _get_conversations_as_string(df):
    df_documents = df[df.text != '/greet']
    df_documents = df_documents[
        df_documents['text'].apply(lambda x: isinstance(x, str) and _filter_text(x))]
    df_documents = df_documents.groupby('conversation_id')['text'].agg(lambda x: ' '.join(x)).reset_index()
    conversations = df_documents['text'].tolist()
    return [_clean_text(conversation) for conversation in conversations]


def get_topic_graph(df):
    conversations = _get_conversations_as_string(df)
    topics, probs = topic_model.fit_transform(conversations)
    graph = dcc.Graph(id='topic-graph', figure=topic_model.visualize_topics())

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Topics", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
