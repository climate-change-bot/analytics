import dash_bootstrap_components as dbc
from dash import html, dash_table


def get_ranking(df_intents):
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        dash_table.DataTable(df_intents.to_dict('records'),
                                             [{"name": i, "id": i} for i in df_intents.columns],
                                             style_cell_conditional=[
                                                 {
                                                     'if': {'column_id': df_intents.columns[0]},
                                                     'textAlign': 'left',
                                                 }
                                             ]
                                             )]),
                style={
                    "maxHeight": "400px",
                    "overflowY": "auto",
                }
            )
        ])
