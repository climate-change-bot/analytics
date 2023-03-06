from dash import dash, html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

navbar = dbc.NavbarSimple(
    children=[],
    brand="Climate Change Bot",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
)

app.layout = html.Div(children=[
    navbar,
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
