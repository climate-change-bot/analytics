import os
import glob
import yaml
import re

_nlu_dir = os.environ.get('CHATBOT_NLU_DIR', '/home/roger/Documents/HSLU/Masterthesis/code/chatbot/rasa/data/nlu')


def _clean_intents(intents):
    for intent in intents:
        intent['examples'] = re.sub(r'\[(.*?)\]\{.*?\}', r'\1', intent['examples'])
        intent['examples'] = intent['examples'].split('\n-')
        for index, example in enumerate(intent['examples']):
            intent['examples'][index] = example.lstrip('-').strip().lower()
    return intents


def get_intents_as_list(intents):
    intents_as_list = []
    for intent in intents:
        intents_as_list.extend(intent['examples'])
    return intents_as_list


def get_intents():
    nlu_yaml_files = glob.glob(os.path.join(_nlu_dir, "**/*.yml"), recursive=True)
    intents = []

    for yaml_file in nlu_yaml_files:
        with open(yaml_file, "r") as f:
            yaml_nlu = yaml.safe_load(f)
            for nlu in yaml_nlu['nlu']:
                if 'examples' in nlu and 'intent' in nlu:
                    intents.append(nlu)
    intents = _clean_intents(intents)
    return intents


def get_chatgpt_intents(df, intents):
    intents_as_list = get_intents_as_list(intents)
    df_chatgpt = df[(df.type_name == 'user') & (df.timestamp > 1677063600) & (df.intent_name == 'nlu_fallback')]
    return [text for text in df_chatgpt['text'].tolist() if type(text) == 'str' and text.lower() not in intents_as_list]
