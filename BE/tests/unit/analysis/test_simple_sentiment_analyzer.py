from unittest import TestCase

from BE.src.analysis.nlp_models.sentiment_analysis.simple_sentiment_analyser import simple_sentiment_analyzer


class TestSentimentAnalysis(TestCase):

    def test_positive_sentiment(self):
        sentence = "Ich liebe diesen Film, er ist grossartig!"
        expected_score = 1.0
        score = simple_sentiment_analyzer(sentence).polarity

        self.assertAlmostEqual(expected_score, score, delta=0.1)

    def test_negative_sentiment(self):
        sentence = "Dieser Film ist so langweilig!"
        expected_score = -1.0
        score = simple_sentiment_analyzer(sentence).polarity

        self.assertAlmostEqual(expected_score, score, delta=0.1)

    def test_neutral_sentiment(self):
        sentence = "Ich habe einen Film gesehen."
        expected_score = 0.0
        score = simple_sentiment_analyzer(sentence).polarity

        self.assertAlmostEqual(expected_score, score, delta=0.1)
