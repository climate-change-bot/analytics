from sentence_transformers import SentenceTransformer, util
from climate_change_bot.analytics.components.intent.intents import get_intents_as_list

model = SentenceTransformer('all-MiniLM-L6-v2')


def _get_intent(intents, intent_question):
    for intent in intents:
        if intent_question in intent['examples']:
            return intent['intent']


def _intent_to_chatgpt(cos_distance, index_1, index_2, all_sentences, index_split_intent, intents):
    if (index_1 < index_split_intent) and (index_2 >= index_split_intent):
        intent_name = _get_intent(intents, all_sentences[index_1])
        return intent_name, {'cos_distance': cos_distance, 'intent_text': all_sentences[index_1],
                             'text_for_chatgpt': all_sentences[index_2]}
    return None, None


def get_similarities(intents, all_chatgpt_intents):
    intents_as_list = get_intents_as_list(intents)
    combined = intents_as_list + all_chatgpt_intents

    paraphrases = util.paraphrase_mining(model, combined, top_k=10)

    similarities = {}
    for paraphrase in paraphrases:
        cos_distance = paraphrase[0]
        index_1 = paraphrase[1]
        index_2 = paraphrase[2]
        intent_name, similarity = _intent_to_chatgpt(cos_distance, index_1, index_2, combined, len(intents_as_list),
                                                     intents)
        if intent_name and similarity['cos_distance'] >= 0.6:
            if intent_name in similarities:
                similarities[intent_name].append(similarity)
            else:
                similarities[intent_name] = [similarity]

    return similarities
