from dash import dash, html, dcc, DiskcacheManager
import pandas as pd
import diskcache
import os
import dash_bootstrap_components as dbc

from uuid import uuid4

_file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')

df = pd.read_excel(_file_name)

df['timestamp_datetime'] = pd.to_datetime(df['timestamp'], unit='s')
df['date'] = df['timestamp_datetime'].dt.date

# Caching of views.
launch_uid = uuid4()
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(
    cache, cache_by=[lambda: launch_uid], expire=60
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True,
                background_callback_manager=background_callback_manager)
app.config.suppress_callback_exceptions = True

navbar = dbc.NavbarSimple(
    children=[],
    brand="Climate Change Bot Analytics",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
)

app.layout = html.Div(children=[
    dcc.Store(id='global-data', data=df.to_dict('records')),
    dcc.Store(id='global-data-not-filtered', data=df.to_dict('records')),
    navbar,
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
