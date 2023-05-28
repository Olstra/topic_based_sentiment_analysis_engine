from textblob_de import TextBlobDE as TextBlob


def simple_sentiment_analyzer(sentence: str) -> float:
    text_sentiment = TextBlob(sentence).polarity

    return text_sentiment


if __name__ == '__main__':
    example_sentence = "Im Moment ist mein Alltag eher eintönig, da mein Mann für Ausflüge zu wenig mobil ist. "
    print(simple_sentiment_analyzer(example_sentence))
