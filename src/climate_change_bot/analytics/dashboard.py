from dash import dash, html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div(children=[
    html.H1('Chatbot Analysis'),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
