import dash
from dash import html

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.intent.ranking import get_ranking
from climate_change_bot import df

dash.register_page(__name__, path='/intents')

df_intents = df[(df.intent_name != 'nlu_fallback') & (df.intent_name != 'greet') & (df.type_name == 'user')]
df_intent_ranking = df_intents.groupby(['intent_name']).size().reset_index(name='counts').sort_values(by='counts',
                                                                                                      ascending=False)

layout_content = [
    get_ranking(df_intent_ranking)
]

content = get_content(layout_content)
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])
