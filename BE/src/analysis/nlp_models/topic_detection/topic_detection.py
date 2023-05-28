"""
Make use of multiple topic detection techniques to extract topics with more accuracy.
"""
from BE.src.analysis.nlp_models.topic_detection.simple_topic_detection import simple_detect_topics
from BE.src.analysis.openai_model.openai_model import OpenaiModel
from BE.src.preprocessing.lemmatizer import lemmatize


def extract_topics(sentence: str) -> list[str]:
    """
    Pick topics that appear in simple answer and GPT answer for increased accuracy
    If no congruent topics are found, return simple model answer, which is more appropriate in this application domain
    (which includes Swiss-German words and many typos). We opt for the simple answer because e.g. the GPT answer
    translates "2 Manderinli" (2 mandarins) to "2 Männer" (2 men), so more meaning is preserved by returning simpel answer.
    """

    simple_model_answer = simple_detect_topics(sentence)

    gpt_answer = get_gpt_topics(sentence)

    result = []

    for topic in gpt_answer:
        if topic.lower() in simple_model_answer:
            result.append(topic)

    if result is None:
        result = simple_model_answer

    return result


def get_gpt_topics(sentence: str) -> list[str]:

    gpt_model = OpenaiModel()

    result = gpt_model.get_topics(sentence)

    # parse gpt answer to ensure consistency
    result = result.replace("output:", "")
    result = result.replace(" ", "").split(",")
    result = lemmatize(result)

    return result


if __name__ == '__main__':
    example_text = """Weiterhin auf 150W Max / 125W Durchschnitt. Steigerung liegt aber noch nicht drinnen. Vielleicht nächste Woche."""
    print(extract_topics(example_text))
