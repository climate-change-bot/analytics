import pandas as pd
import csv
import os

_file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')
_model_versions_name = os.environ.get('MODEL_VERSIONS', '../../../model_versions.csv')
_model_versions = {}

with open(_model_versions_name) as csv_file:
    model_version_reader = csv.reader(csv_file, delimiter=';')
    next(model_version_reader, None)
    for row in model_version_reader:
        _model_versions[row[0]] = {'chatbot_version': row[1], 'rasa_version': row[2]}

df = pd.read_excel(_file_name)


def get_version(model_id):
    if model_id in _model_versions:
        return _model_versions[model_id]
    return {'chatbot_version': 'None', 'rasa_version': 'None'}
