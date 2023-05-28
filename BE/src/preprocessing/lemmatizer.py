from typing import List

import spacy


def lemmatize(texts: List[str], allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]) -> List[str]:

    nlp = spacy.load("de_core_news_md", disable=["parser", "ner"])

    result = []

    for text in texts:
        doc = nlp(text)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_.lower())
        final = " ".join(new_text)
        result.append(final)

    return result


def lemmatize_sentence(sentence: str):
    nlp = spacy.load("de_core_news_md")
    doc = nlp(sentence)
    result = ""
    for token in doc:
        result = token.lemma_.lower() + " "  # in case multiple words
    return result.strip()  # delete last " " in case only 1 word


if __name__ == '__main__':
    example = "Alle dies Hunde"
    print(lemmatize_sentence(example))
