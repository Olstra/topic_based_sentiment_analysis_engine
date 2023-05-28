from unittest import TestCase

from BE.src.analysis.nlp_models.absa.absa_simple import aspect_sentiment_analysis
from BE.src.preprocessing.data_cleaner import clean_sentence
from BE.src.preprocessing.emojis_parser import emojis_to_description


def preprocess(sentence: str) -> str:
    sentence = clean_sentence(sentence)
    sentence = emojis_to_description(sentence)
    return sentence


class TestSentimentAnalysis(TestCase):

    def test_sentence_with_emojis(self):
        data = "die Zwischenmahlzeit bestand aus einem 🍎"

        data = preprocess(data)

        expected_aspects = ["Zwischenmahlzeit", "Apfel"]
        expected_sentiments = [0, 0]

        result = aspect_sentiment_analysis(data)

        for e in result:
            self.assertIn(e.topic, expected_aspects)
            self.assertIn(e.sentiment, expected_sentiments)
