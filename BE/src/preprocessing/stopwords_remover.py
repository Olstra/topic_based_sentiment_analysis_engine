import nltk
from nltk.corpus import stopwords as nltk_stopwords


def remove_stopwords(text: list[str]) -> list[str]:
    result = []
    nltk.download('stopwords')
    stopwords = nltk_stopwords.words('german')

    for sentence in text:
        words = sentence.split()
        new_sentence = ""
        for word in words:
            if word not in stopwords:
                new_sentence += word + " "
        result.append(new_sentence.strip())

    return result
