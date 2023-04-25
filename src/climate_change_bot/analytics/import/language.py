from ftlangdetect import detect
from tqdm import tqdm


def add_language(df):
    print("Add Languages")
    languages = []
    ignored_intents = ['greet', 'start_quiz', 'quiz_answer']
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if isinstance(row['text'], str) and len(row['text'].strip()) and row['intent_name'] not in ignored_intents:
            detected_language = detect(text=row['text'].replace("\n", ""), low_memory=False)
            languages.append(detected_language['lang'])
        else:
            languages.append('de')

    df['language'] = languages
