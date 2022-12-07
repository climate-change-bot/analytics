import os
import pandas as pd
import json
from connect_db import create_connection

DATA_DIRECTORY = './../../../../data/'


def add_data(cell, name):
    data = json.loads(cell[0])
    if name in data:
        return data[name]


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


def import_events():
    db_name = os.environ.get('DB_NAME', 'rasa')
    db_user = os.environ.get('DB_User', 'rasa')
    db_password = os.environ.get('DB_PASSWORD', 'localhost')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '5432')
    output_file_name = os.environ.get('OUTPUT_FILE_NAME', 'conversations.xlsx')

    with create_connection(db_name, db_user, db_password, db_host, db_port) as con:
        sql_query = pd.read_sql("SELECT * FROM events WHERE type_name = 'user' OR type_name = 'bot'", con)
        df = pd.DataFrame(sql_query,
                          columns=['sender_id', 'type_name', 'timestamp', 'intent_name', 'action_name', 'data'])

        # Clean Data
        df['model_id'] = df[['data']].apply(add_model_id, axis=1)
        df['text'] = df[['data']].apply(lambda x: add_data(x, 'text'), axis=1)
        df['intent'] = df[['data']].apply(lambda x: add_model_intent(x, 'name'), axis=1)
        df['intent_confidence'] = df[['data']].apply(lambda x: add_model_intent(x, 'confidence'), axis=1)
        df['input_channel'] = df[['data']].apply(lambda x: add_data(x, 'input_channel'), axis=1)
        df['intent_ranking'] = df[['data']].apply(add_model_intent_ranking, axis=1)

        df['number_of_chats'] = df.groupby('sender_id').sender_id.transform('size')
        df = df[df['number_of_chats'] > 2]

        df = df.drop('data', axis=1)

        df = df.sort_values(by='timestamp')

        if not os.path.exists(DATA_DIRECTORY):
            os.mkdir(DATA_DIRECTORY)
        with pd.ExcelWriter(f'{DATA_DIRECTORY}{output_file_name}', engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name='conversations')


if __name__ == "__main__":
    import_events()
