import dash_bootstrap_components as dbc
from sentence_transformers import SentenceTransformer, util
from dash import html

model = SentenceTransformer('all-MiniLM-L6-v2')


def _get_intents_examples(all_intents):
    examples = []
    for intent in all_intents:
        examples.extend(intent['examples'])
    return examples


def get_cluster_card(df, all_intents):
    items = []
    examples = _get_intents_examples(all_intents)
    df_user_text = df[(df.intent_name == 'nlu_fallback') & (df.type_name == 'user')]
    user_text = [x.lower().replace('?', '').replace('.', '').replace('!', '') for x in df_user_text['text']]
    user_text = list(set([x for x in user_text if x not in examples]))
    corpus_embeddings = model.encode(user_text, batch_size=64, show_progress_bar=True, convert_to_tensor=True)
    clusters = util.community_detection(corpus_embeddings, min_community_size=5, threshold=0.85)
    for index, cluster in enumerate(clusters):
        list_group_items = []
        for cluster_item in cluster:
            list_group_items.append(dbc.ListGroupItem(user_text[cluster_item]))

        list_group = dbc.ListGroup(list_group_items)
        items.append(dbc.AccordionItem([list_group], title=f'Cluster {index + 1}'))

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Clusters", className="mb-1")]),
                dbc.CardBody(
                    [
                        dbc.Accordion(items, always_open=True)

                    ], style={
                        "maxHeight": "800px",
                        "overflowY": "auto"
                    })])], style={"padding-bottom": "200px"})
