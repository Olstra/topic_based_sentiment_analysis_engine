import time

import spacy

from BE.src.DTOs.topicSentimentDTO import TopicSentimentDTO
from BE.src.analysis.nlp_models.sentiment_analysis.roberta_sentiment_analyzer import analyze_sentiment
from BE.src.analysis.nlp_models.sentiment_analysis.simple_sentiment_analyser import simple_sentiment_analyzer
from BE.src.analysis.openai_model.openai_model import OpenaiModel
from BE.src.preprocessing.data_cleaner import clean_sentence
from BE.src.preprocessing.emojis_parser import emojis_to_description, remove_emojis_for_topic_detection


def aspect_sentiment_analysis(sentence: str) -> list[TopicSentimentDTO]:

    nlp = spacy.load("de_core_news_md")
    doc = nlp(sentence)

    result = []

    # Extract aspects and their corresponding sentiment scores
    for chunk in doc.noun_chunks:

        text_with_emojis = emojis_to_description(sentence)

        parsed_topic_name = parse_topic_name(chunk.text)

        if parsed_topic_name != "" or None:
            new = TopicSentimentDTO(
                topic=parsed_topic_name,
                sentiment=calculate_sentiment(text_with_emojis)
            )
            result.append(new)

            # wait 20s due to ChatGPT restriction to 3 requests per minute
            print("Waiting 20 seconds...")
            time.sleep(20)

    return result


def parse_topic_name(text: str) -> str:
    allowed_postags  = ["NOUN"]

    nlp = spacy.load("de_core_news_md", disable=["parser", "ner"])

    text = remove_emojis_for_topic_detection(text)

    doc = nlp(text)

    result = ""

    for token in doc:
        if token.pos_ in allowed_postags:
            result += token.lemma_ + " "

    return result.strip()


def calculate_sentiment(sentence: str) -> float:
    gpt_model = OpenaiModel()

    # calculate answers from different models
    simple_model_answer = simple_sentiment_analyzer(sentence)
    nlp_answer = analyze_sentiment(sentence)
    gpt_answer = gpt_model.get_sentiment(sentence)

    print(f"Sentence{sentence}\n"
          f"GPT: {gpt_answer} SIMPLE: {simple_model_answer} NLP: {nlp_answer}")

    weights     = [0.2,                 0.3,        0.5]
    all_answers = [simple_model_answer, nlp_answer, gpt_answer]

    if gpt_answer is None:
        # disregard GPTs answer in case we got a bad answer from the model
        weights.pop()
        all_answers.pop()

    # calculate weighted average
    all_answers = [all_answers[i] * weights[i] for i in range(len(weights))]

    weighted_avg_answer = sum(answer for answer in all_answers)

    return weighted_avg_answer


if __name__ == '__main__':
    data = "yes die kilo sind geschafft😊😊😊️"

    # preprocess
    data = clean_sentence(data)

    print(calculate_sentiment("toll"))
