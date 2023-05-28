"""
Perform topic based sentiment analysis
"""
import logging
import time

import nltk

from BE.src.DTOs.topicSentimentDTO import TopicSentimentDTO
from BE.src.analysis.nlp_models.absa.absa_simple import aspect_sentiment_analysis
from BE.src.analysis.nlp_models.topic_detection.topic_detection import extract_topics
from BE.src.preprocessing.data_cleaner import clean_sentence
from BE.src.preprocessing.emojis_parser import remove_emojis_for_topic_detection
from BE.src.preprocessing.lemmatizer import lemmatize, lemmatize_sentence
from BE.src.preprocessing.stopwords_remover import remove_stopwords


def topic_based_sentiment_analysis(sentence: str) -> list[TopicSentimentDTO]:
    """
    Pick topics that were detected by our topic analysis process and the ABSA function for more accuracy.
    If no overlapping topics are found, return ABSA function result as default "guess" for topics.
    The sentiments are calculated by the ABSA function.
    """

    # simple text preprocessing
    sentence = clean_sentence(sentence)

    absa = aspect_sentiment_analysis(sentence)

    # preprocess further for topic detection
    sentence = remove_emojis_for_topic_detection(sentence)
    sentence = remove_stopwords([sentence])
    sentence = lemmatize(sentence)
    sentence = " ".join(sentence)  # convert sentence back to string

    topics = extract_topics(sentence)
    topics = [topic.lower() for topic in topics]

    result = []

    for entry in absa:
        entry.topic = lemmatize_sentence(entry.topic)
        if entry.topic in topics:
            result.append(entry)

    if not result:
        logging.info("No overlapping topics found, returning simple ABSA answer...")

        # wait 20s due to ChatGPT restriction to 3 requests per minute
        print("Waiting 20 seconds...")
        time.sleep(20)

        return absa

    # wait 20s due to ChatGPT restriction to 3 requests per minute
    print("Waiting 20 seconds...")
    time.sleep(20)

    return result


if __name__ == '__main__':
    example_text = "Suche nach der neuen Wölfin im Tierpark👍😀 19000 Schritte 🎉"
    print(topic_based_sentiment_analysis(example_text))
