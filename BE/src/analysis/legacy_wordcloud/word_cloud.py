"""
Word cloud generator where:
- word size = how often that word was named
- word color is determined by the associated sentiment with that word
(e.g. negative sentiment -> red color)
"""
import os
from typing import List
from BE.src.DTOs.topicSentimentDTO import TopicSentimentDTO
from BE.src.main import db_handler
from BE.src.analysis.legacy_wordcloud.valence_entries_parser import parse_valence_entries
from wordcloud import WordCloud
from BE.src.config import config_instance


def get_data(patient_id: int):
    raw_data = db_handler.get_patient_topics_sentiments(patient_id)
    return parse_valence_entries(raw_data)


def parse_wordcloud_input(data: List[TopicSentimentDTO]):
    wordcloud_input = {}
    for e in data:
        wordcloud_input[e.topic] = float(e.nr_of_occurrences)
    return wordcloud_input


def generate_color_map(data: List[TopicSentimentDTO]):
    colors = {"positive": "green", "negative": "red", "neutral": "grey"}
    color_map = {}
    for e in data:
        color_map[e.topic] = colors[e.sentiment]
    return color_map


def set_word_colors(word, color_map):
    return color_map[word]


def save_wordcloud_image(patient_id: int, wordcloud: WordCloud):
    # create the custom folder if it doesn't exist
    path = config_instance.wc_location
    if not os.path.exists(path):
        os.makedirs(path)
    # save image to custom folder
    wordcloud.to_file(os.path.join(path, f'Patient_{patient_id}-wordcloud.png'))


def generate_wordcloud(patient_id: int, width: int = 800, height: int = 400):
    # prepare data for wordcloud
    patient_data = get_data(patient_id)
    wc_input = parse_wordcloud_input(patient_data)
    colors = generate_color_map(patient_data)

    # create wordcloud
    wordcloud = WordCloud(background_color="white", width=width, height=height)
    wordcloud.generate_from_frequencies(wc_input)

    wordcloud.recolor(color_func=lambda word, font_size, position, orientation, random_state=None,
                                        **kwargs: set_word_colors(word, colors))

    save_wordcloud_image(patient_id, wordcloud)


if __name__ == '__main__':
    example_patient_id = 2
    generate_wordcloud(example_patient_id)
