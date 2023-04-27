def get_turns(df):
    df_turns = df[df.intent != 'greet']
    turn_counts = df_turns.groupby('conversation_id').apply(lambda group: (group['type_name'] == 'user').sum())
    max_turns_count = turn_counts.max()
    total_turns = turn_counts.sum()
    return total_turns, max_turns_count, turn_counts
