from dash import dash, html, dcc, DiskcacheManager
import diskcache
import dash_bootstrap_components as dbc

from uuid import uuid4

# Caching of views.
launch_uid = uuid4()
cache = diskcache.Cache("./cache")

background_callback_manager = DiskcacheManager(
    cache, cache_by=[lambda: launch_uid], expire=60
)
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY], use_pages=True,
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
    dcc.Store(id='signal-global-data'),
    dcc.Store(id='signal-global-data-not-filtered'),
    navbar,
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True, threaded=False)
