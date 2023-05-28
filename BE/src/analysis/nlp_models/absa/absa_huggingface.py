from pyabsa import AspectTermExtraction as ATEPC

from BE.src.DTOs.topicSentimentDTO import TopicSentimentDTO
from BE.src.preprocessing.data_cleaner import clean_sentence
from BE.src.preprocessing.emojis_parser import emojis_to_description
from BE.src.preprocessing.lemmatizer import lemmatize_sentence
from BE.src.preprocessing.translator import translate


def absa_huggingface(sentence: str, model_lang="multilingual") -> list[TopicSentimentDTO]:

    # setup model
    config = (
        ATEPC.ATEPCConfigManager.get_atepc_config_english() if model_lang == "english" else ATEPC.ATEPCConfigManager.get_atepc_config_multilingual()
    )
    config.model = ATEPC.ATEPCModelList.FAST_LCF_ATEPC
    aspect_extractor = ATEPC.AspectExtractor(checkpoint="english" if model_lang == "english" else "multilingual")

    # preprocess
    sentence = clean_sentence(sentence)
    sentence = emojis_to_description(sentence)

    if model_lang.lower() == "english":
        sentence = translate(sentence)

    prediction = aspect_extractor.predict(
        text=sentence,
        ignore_error=True,  # ignore an invalid example, if it is False, invalid examples will raise Exceptions
        eval_batch_size=32,
    )

    # parse result(s)
    result = []
    for i in range(len(prediction["aspect"])):
        aspect = prediction["aspect"][i]
        polarity = get_polarity(prediction, i)

        if model_lang.lower() == "english":
            aspect = translate(aspect, "DE")

        new = TopicSentimentDTO(
            topic=lemmatize_sentence(aspect),
            sentiment=polarity
        )
        result.append(new)

    return result


def get_polarity(prediction: dict, item_index: int) -> float:
    """
    We take the probability of the dominating sentiment and assign it as polarity.
    """
    sentiment = prediction["sentiment"][item_index]
    sentiment_index = map_sentiment_to_index(sentiment)
    polarity = prediction["probs"][item_index][sentiment_index]

    # To ensure consistent behavior and simplify the handling of sentiments, we set the default polarity value for
    # neutral to 0.0 and for negative sentiments we use negative polarity.
    if sentiment == "Neutral":
        polarity = 0.0
    elif sentiment == "Negative":
        polarity *= -1

    return polarity


def map_sentiment_to_index(sentiment: str) -> int:
    sentiment_map = {"Positive": 2, "Neutral": 1, "Negative": 0}
    index = sentiment_map[sentiment]
    return index


if __name__ == '__main__':
    data = """leide habe ich heute immer noch starke halsschmerzen. deshalb fühle ich mich nicht ganz so gut. 
 zu frühstück heute ein fleischkäseparisette und ein capuchino. 
 mittags nichts da wir noch die wohnunh sauber machen mussten. jedoch zwischendurch schoggistängeli. 
 abends ghackets mit hörnli und apfelmus"""

    # preprocess
    data = clean_sentence(data)
    data = emojis_to_description(data)

    print(absa_huggingface(data, model_lang="english"))
