"""
Collection of useful functions when performing NLP tasks.
"""

from typing import List


def get_words_as_string(sentences: List[str]) -> str:
    result = ""
    for sentence in sentences:
        for word in sentence.split():
            result += word + " "
    return result.strip()


def get_words_as_list(sentences: List[str]) -> List[str]:
    result = []
    for sentence in sentences:
        for word in sentence.split():
            result.append(word)
    return result
