import dash_bootstrap_components as dbc
from dash import html


def get_similarity_card(similarities):
    items = []
    for similarity in similarities:
        table_header = [
            html.Thead(html.Tr([html.Th("Cosinus Distance"), html.Th("Intent Text"), html.Th("Text to ChatGPT")]))
        ]

        rows = [html.Tr([html.Td(x['cos_distance']), html.Td(x['intent_text']), html.Td(x['text_for_chatgpt'])]) for x
                in similarities[similarity]]

        table_body = [html.Tbody(rows)]

        table = dbc.Table(table_header + table_body, bordered=True)
        items.append(dbc.AccordionItem([table], title=similarity))

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Similarity to Request sent to ChatGPT", className="mb-1")]),
                dbc.CardBody(
                    [
                        # html.H5("Intent Similarity to Request sent to ChatGPT", className="mb-1",
                        #         style={"padding-bottom": "8px"}),
                        dbc.Accordion(items, always_open=True)

                    ], style={
                        "maxHeight": "400px",
                        "overflowY": "auto"
                    })])])
