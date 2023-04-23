def add_column_is_quiz(df):
    print("Add is quiz column")
    is_quiz = []
    is_quiz_sequence = {}
    for row in df.to_dict('records'):
        if row['sender_id'] not in is_quiz_sequence:
            is_quiz_sequence[row['sender_id']] = 0

        if row['type_name'] == 'user':
            if row['intent'] == 'start_quiz':
                is_quiz_sequence[row['sender_id']] = 1
            elif row['intent'] != 'quiz_answer':
                is_quiz_sequence[row['sender_id']] = 0
        is_quiz.append(is_quiz_sequence[row['sender_id']])
    df['is_quiz'] = is_quiz
