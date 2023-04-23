from germansentiment import SentimentModel
from tqdm import tqdm


def _predict(df):
    model = SentimentModel()
    invalid_intents = ['greet', 'start_quiz', 'quiz_answer']
    probabilities = {'positive': [], 'negative': [], 'neutral': []}
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if row['type_name'] == 'user' and isinstance(row['text'], str) and not row['intent_name'] in invalid_intents:
            classes, probabilities_row = model.predict_sentiment([row['text']], output_probabilities=True)
            probabilities[probabilities_row[0][0][0]].append(probabilities_row[0][0][1])
            probabilities[probabilities_row[0][1][0]].append(probabilities_row[0][1][1])
            probabilities[probabilities_row[0][2][0]].append(probabilities_row[0][2][1])
        else:
            probabilities['positive'].append(None)
            probabilities['negative'].append(None)
            probabilities['neutral'].append(None)
    return probabilities['positive'], probabilities['negative'], probabilities['neutral']


def add_sentiment(df):
    print("Add sentiment columns")
    positive, negative, neutral = _predict(df)
    df['positive'] = positive
    df['negative'] = negative
    df['neutral'] = neutral
