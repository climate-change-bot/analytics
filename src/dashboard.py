from dash import dash, html
import dash_bootstrap_components as dbc
import pandas as pd
import os

from components.conversation_overview import get_conversations

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

file_name = os.environ.get('FILE_NAME', '../data/conversations_prod.xlsx')

df = pd.read_excel(file_name)

df['number_of_chats'] = df.groupby('sender_id').sender_id.transform('size')
df_conversation_overview = df.drop_duplicates(subset=['sender_id'])
df_conversation_overview = df_conversation_overview.sort_values(by=['timestamp'], ascending=False)

app.layout = html.Div(children=[
    html.H1(children='Chatbot Analysis'),
    get_conversations(df_conversation_overview)
])

if __name__ == '__main__':
    app.run_server(debug=True)
