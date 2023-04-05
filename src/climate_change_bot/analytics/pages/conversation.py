import dash
from dash import html

from climate_change_bot import df
from climate_change_bot import get_version
from climate_change_bot.analytics.pages.base import get_content, get_sidebar
from climate_change_bot.analytics.components.conversation_messages import get_conversation_messages
from climate_change_bot.analytics.components.conversation_messages import get_side_bar

dash.register_page(__name__, path_template="/conversation/<conversation_id>")


def layout(conversation_id=None):
    if conversation_id:
        df_conversation = df[df['conversation_id'] == int(conversation_id)]
        model_versions = get_version(df_conversation.iloc[0]['model_id'])

        content = get_content([get_conversation_messages(df_conversation)])
        sidebar = get_sidebar(get_side_bar(df_conversation, model_versions))

        return html.Div(children=[
            sidebar, content
        ])
