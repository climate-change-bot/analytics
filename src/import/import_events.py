import os
import pandas as pd
from connect_db import create_connection

DATA_DIRECTORY = './../../data/'


def import_events():
    db_name = os.environ.get('DB_NAME', 'rasa')
    db_user = os.environ.get('DB_User', 'rasa')
    db_password = os.environ.get('DB_PASSWORD', 'localhost')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '5432')
    with create_connection(db_name, db_user, db_password, db_host, db_port) as con:
        sql_query = pd.read_sql('SELECT * FROM events', con)
        df = pd.DataFrame(sql_query,
                          columns=['sender_id', 'type_name', 'timestamp', 'intent_name', 'action_name', 'data'])
        os.mkdir(DATA_DIRECTORY)
        df.to_excel(f'{DATA_DIRECTORY}conversations.xlsx', sheet_name='conversations')


if __name__ == "__main__":
    import_events()
