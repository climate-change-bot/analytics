import os
import csv

_model_versions_name = os.environ.get('MODEL_VERSIONS', '../../../../model_versions.csv')


def add_model_and_rasa_version(df):
    print("Add model and rasa version")
    model_versions = {}
    chatbot_versions = []
    rasa_versions = []

    with open(_model_versions_name) as csv_file:
        model_version_reader = csv.reader(csv_file, delimiter=';')
        next(model_version_reader, None)
        for row in model_version_reader:
            model_versions[row[0]] = {'chatbot_version': row[1], 'rasa_version': row[2]}

    for row in df.to_dict('records'):
        if row['model_id'] in model_versions:
            chatbot_versions.append(model_versions[row['model_id']]['chatbot_version'])
            rasa_versions.append(model_versions[row['model_id']]['rasa_version'])
        else:
            raise ImportError(f"Model ID not in versions: model_id {row['model_id']}")

    df['chatbot_version'] = chatbot_versions
    df['rasa_version'] = rasa_versions

