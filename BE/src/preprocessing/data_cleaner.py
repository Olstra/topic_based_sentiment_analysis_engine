import re
import string


def clean_sentences(text: list[str]) -> list[str]:
    result = []

    for sentence in text:
        cleaned_sentence = clean_sentence(sentence)
        result.append(cleaned_sentence)

    return result


def clean_sentence(sentence: str) -> str:
    """
    This function removes irrelevant information for the analysis from the text.
    """
    sentence = sentence.lower()

    # remove square brackets
    sentence = re.sub(r'\[.*?\]', '', sentence)

    # remove punctuation
    sentence = re.sub(r'[%s]' % re.escape(string.punctuation), '', sentence)

    sentence = re.sub(r'\b(km|m|cm|mm)\b', '', sentence)

    # remove words containing numbers
    sentence = re.sub(r'\w*\d\w*', '', sentence)

    # only 1 space between words
    sentence = sentence.strip()
    sentence = sentence.replace("\n|\t", " ")
    sentence = " ".join(sentence.split())

    return sentence


if __name__ == '__main__':
    example_sentence = "nur 80% 1 Mandelgipfel\n\t 1 Würfelzucker\n\t1 Vieille Prune"
    print(clean_sentence(example_sentence))
