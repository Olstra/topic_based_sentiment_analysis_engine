"""
Convert emojis to their textual representation.
"""
import re

import emoji


def emojis_to_description(sentence: str) -> str:
    """
    about: replace_emoji(): replace(str, dict) -> str
    """

    sentence = add_space_between_word_and_emoji(sentence)

    result = emoji.replace_emoji(sentence, replace=replace_emoji_chars)

    return result


def replace_emoji_chars(emoji_chars: str, emoji_information: dict) -> str:
    """
    A function that replaces the emoji characters with their corresponding description.
    :return: The description of the emoji after removing the underscores, colons, and skin color.
    """
    lang = "de"
    emoji_description = ' '.join(emoji_information[lang].split('_')).strip(':')

    # Check if skin tone modifier is present in the emoji description. If yes remove it.
    pattern = r"(mittelhelle|mittlere|mitteldunkle|helle|dunkle)\s+hautfarbe"
    emoji_description = re.sub(pattern, "", emoji_description, flags=re.IGNORECASE)

    pattern = r"gesicht"
    emoji_description = re.sub(pattern, "", emoji_description, flags=re.IGNORECASE)

    return emoji_description


def add_space_between_word_and_emoji(sentence: str):
    """
    Function that ensures there is 1 space between an emoji and a word.
    This way we don't get problems in this regard when performing topic detection.
    """

    pattern = r'(\w)([^\w\s])'

    result = re.sub(pattern, r'\1 \2', sentence)

    return result


def remove_emojis(sentence: str):
    result = emoji.replace_emoji(sentence, replace="")

    return result


def remove_emojis_for_topic_detection(sentence: str):
    """
    With this emojis parsing function we remove all emojis that are the most likely not an aspect of the sentence
    provided as input.
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # smileys
                               u"\U0001F44D-\U0001F44F"  # hand gestures
                               u"\U0001F3FB-\U0001F3FF"  # skin colors
                               u"\U00002702-\U000027B0"  # other miscellaneous
                               "]+", flags=re.UNICODE)

    result = emoji_pattern.sub(r'', sentence)

    return result


if __name__ == '__main__':
    example_text = "🍚j'adore❤️, die 👍d😊😊😊 👍🏼bestand aus einem 🍎aber dazu 😤"
    print(remove_emojis_for_topic_detection(example_text))
