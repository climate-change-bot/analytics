from climate_change_bot.analytics.store import TIME_CHAT_GPT_USED


def get_chatgpt_answers(df):
    chatgpt_index = df[
        (df.type_name == 'user') & (df.timestamp > TIME_CHAT_GPT_USED) & (df.intent_name == 'nlu_fallback')].index
    next_row_indices = [index + 1 for index in chatgpt_index]
    df_chatgpt_answer = df.iloc[next_row_indices]
    df_chatgpt_answer = df_chatgpt_answer[df_chatgpt_answer.is_climate_change_related == 1]
    df_chatgpt_answer.reset_index(drop=True, inplace=True)
    return df_chatgpt_answer
