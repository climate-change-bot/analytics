import dash
from dash import html

from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.intent.ranking import get_ranking
from climate_change_bot.analytics.components.intent.intents import get_intents, get_chatgpt_intents
from climate_change_bot.analytics.components.intent.similarity import get_similarities
from climate_change_bot.analytics.components.intent.similarity_card import get_similarity_card
from climate_change_bot import df

dash.register_page(__name__, path='/intents')

df_intents = df[(df.intent_name != 'nlu_fallback') & (df.intent_name != 'greet') & (df.type_name == 'user')]
df_intent_ranking = df_intents.groupby(['intent_name']).size().reset_index(name='counts').sort_values(by='counts',
                                                                                                      ascending=False)

all_intents = get_intents()
all_chatgpt_intents = get_chatgpt_intents(df, all_intents)
similarities = get_similarities(all_intents, all_chatgpt_intents)

layout_content = [
    get_ranking(df_intent_ranking), get_similarity_card(similarities)
]

content = get_content(layout_content)
sidebar = get_sidebar()

layout = html.Div(children=[
    sidebar, content
])
