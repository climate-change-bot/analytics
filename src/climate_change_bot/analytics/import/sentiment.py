from germansentiment import SentimentModel


def _predict(df):
    model = SentimentModel()
    invalid_intents = ['greet', 'start_quiz', 'quiz_answer']
    probabilities = {'positive': [], 'negative': [], 'neutral': []}
    for index, row in df.iterrows():
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
    positive, negative, neutral = _predict(df)
    df['positive'] = positive
    df['negative'] = negative
    df['neutral'] = neutral
