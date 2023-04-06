import dash_bootstrap_components as dbc
from dash import html, dash_table


def get_ranking(df_intents):
    rows = [html.Tr([html.Td(x['intent_name']), html.Td(x['counts'])]) for x in df_intents.to_dict('records')]

    table_body = [html.Tbody(rows)]

    table = dbc.Table(table_body, striped=True)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Ranking", className="mb-1")]),
                dbc.CardBody([table],
                             style={
                                 "maxHeight": "400px",
                                 "overflowY": "auto"
                             })]
            )
        ], style={"padding-bottom": "20px"})
