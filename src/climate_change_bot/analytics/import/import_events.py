import os
import pandas as pd
import json
from connect_db import create_connection
from sentiment import add_sentiment
from quiz import add_column_is_quiz
from version import add_model_and_rasa_version
from testphase import add_testphase
from language import add_language
from chatgpt import add_is_chat_gpt

DATA_DIRECTORY = './../../../../data/'


def add_data(cell, name):
    data = json.loads(cell[0])
    if name in data:
        return data[name]


def add_text(cell):
    data = json.loads(cell[0])
    if 'text' in data and data['text']:
        return data['text']
    elif 'data' in data and 'custom' in data['data'] and 'openai' in data['data']['custom']:
        return data['data']['custom']['text']
    return ""


def add_model_id(cell):
    data = json.loads(cell[0])
    return data['metadata']['model_id']


def add_model_intent(cell, text):
    data = json.loads(cell[0])
    if 'parse_data' in data:
        return data['parse_data']['intent'][text]


def add_model_intent_ranking(cell):
    data = json.loads(cell[0])
    if 'parse_data' in data:
        return data['parse_data']['intent_ranking']


def add_conversation_id(df):
    print("Add conversations ids")
    conversation_id = 0
    conversation_ids = []
    sender_conversation_id = {}
    for row in df.to_dict('records'):
        if row['sender_id'] in sender_conversation_id:
            conversation_ids.append(sender_conversation_id[row['sender_id']])
        else:
            conversation_id += 1
            sender_conversation_id[row['sender_id']] = conversation_id
            conversation_ids.append(conversation_id)
    df['conversation_id'] = conversation_ids


def _get_latest_timestamp(output_file_name):
    if os.path.exists(output_file_name):
        df_output = pd.read_excel(output_file_name, index_col=0)
        return df_output['timestamp'].max() + 0.000001
    return 0


def import_events():
    db_name = os.environ.get('DB_NAME', 'rasa')
    db_user = os.environ.get('DB_User', 'rasa')
    db_password = os.environ.get('DB_PASSWORD', 'localhost')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '5432')
    output_file_name = os.environ.get('OUTPUT_FILE_NAME', 'conversations.xlsx')
    output_file_name = f'{DATA_DIRECTORY}{output_file_name}'
    last_timestamp = _get_latest_timestamp(output_file_name)

    print("Loading from database")

    with create_connection(db_name, db_user, db_password, db_host, db_port) as con:
        sql_query = pd.read_sql(
            f"SELECT * FROM events WHERE (type_name = 'user' OR type_name = 'bot') AND timestamp > {last_timestamp}",
            con)
        df = pd.DataFrame(sql_query,
                          columns=['sender_id', 'type_name', 'timestamp', 'intent_name', 'action_name', 'data'])

        # Clean Data
        print("Clean data")
        df['model_id'] = df[['data']].apply(add_model_id, axis=1)
        df['text'] = df[['data']].apply(lambda x: add_text(x), axis=1)
        df['intent'] = df[['data']].apply(lambda x: add_model_intent(x, 'name'), axis=1)
        df['intent_confidence'] = df[['data']].apply(lambda x: add_model_intent(x, 'confidence'), axis=1)
        df['input_channel'] = df[['data']].apply(lambda x: add_data(x, 'input_channel'), axis=1)
        df['intent_ranking'] = df[['data']].apply(add_model_intent_ranking, axis=1)

        # Add analysis data
        df['is_checked'] = 0  # Answer has been checked by analyst
        df['appropriate_in_context_conversation'] = 0  # Appropriate in the context of the conversation
        df['is_climate_change_related'] = 1  # question/answer is climate change related
        df['chatgpt_correctness_of_content'] = 0  # Chatgpt answer content correct

        df['number_of_chats'] = df.groupby('sender_id').sender_id.transform('size')
        df = df[df['number_of_chats'] > 2]

        df = df.drop('data', axis=1)

        df = df.sort_values(by='timestamp')

        add_is_chat_gpt(df)
        add_language(df)
        add_model_and_rasa_version(df)
        add_testphase(df)
        add_column_is_quiz(df)
        add_sentiment(df)

        if os.path.exists(output_file_name):
            df_previous = pd.read_excel(output_file_name, index_col=0)

            # Add index
            max_previous_index = df_previous['index'].max()
            max_previous_index += 1
            df['index'] = range(max_previous_index, max_previous_index + len(df))

            df = pd.concat([df_previous, df])
        else:
            df['index'] = range(1, len(df) + 1)

        add_conversation_id(df)

        if not os.path.exists(DATA_DIRECTORY):
            os.mkdir(DATA_DIRECTORY)
        with pd.ExcelWriter(output_file_name, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name='conversations')


if __name__ == "__main__":
    import_events()
