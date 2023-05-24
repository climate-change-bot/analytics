from climate_change_bot.analytics.store import TIME_CHAT_GPT_USED


def add_is_chat_gpt(df):
    print("Add is chatgpt")
    is_chat_gpt = []
    is_chat_gpt_answer = False
    for row in df.to_dict('records'):
        if is_chat_gpt_answer and row['type_name'] == 'bot':
            is_chat_gpt.append(1)
        else:
            is_chat_gpt.append(0)

        is_chat_gpt_answer = row['type_name'] == 'user' and row['timestamp'] > TIME_CHAT_GPT_USED and \
                             row['intent_name'] == 'nlu_fallback'

    df['is_chatgpt_answer'] = is_chat_gpt
