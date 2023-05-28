import spacy

from BE.src.preprocessing.data_cleaner import clean_sentence
from BE.src.preprocessing.emojis_parser import emojis_to_description


def simple_detect_topics(sentence: str, allowed_postags=["NOUN", "VERB"]) -> list[str]:
    """
    A very simplistic function that helps detect the topic of a sentence by returning words of that sentence according
    to a predefined POS tag list.
    """

    #sentence = preprocess_simple_topics(sentence)

    nlp = spacy.load("de_core_news_md", disable=["parser", "ner"])

    doc = nlp(sentence)

    result = []

    for token in doc:
        if token.pos_ in allowed_postags:
            result.append(token.lemma_.lower())

    return result


def preprocess_simple_topics(sentence: str) -> str:
    sentence = clean_sentence(sentence)
    sentence = emojis_to_description(sentence)

    return sentence


if __name__ == '__main__':
    text_data = "es gab Dörrbohnen und eine Wurst. lecker geschmeckt"
    print(simple_detect_topics(text_data))
