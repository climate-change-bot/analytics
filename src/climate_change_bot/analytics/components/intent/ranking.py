import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px


def get_ranking(df_intents):
    df_intents_sorted = df_intents.sort_values('counts', ascending=True)
    fig = px.bar(df_intents_sorted, x='counts', y='intent_name', orientation='h')
    fig.update_layout(
        dragmode=None,
        xaxis=dict(title="Counts", fixedrange=True),
        yaxis=dict(title='Intent Name', fixedrange=True),
        plot_bgcolor='white',
        bargap=0.5,
        font=dict(family='Arial', size=12, color='black'),
        height=700
    )
    graph = dcc.Graph(id='intent-ranking-chart', figure=fig)

    return html.Div(
        [
            dbc.Card([
                dbc.CardHeader([html.H5("Intent Ranking", className="mb-1")]),
                dbc.CardBody([graph])]
            )
        ], style={"padding-bottom": "20px"})
