from bertopic import BERTopic
from umap import UMAP

from BE.src.config import config_instance
from BE.src.db_handling.db_handler import db_handler
from BE.src.preprocessing.data_cleaner import clean_sentences
from BE.src.preprocessing.emojis_parser import emojis_to_description
from BE.src.preprocessing.lemmatizer import lemmatize
from BE.src.preprocessing.stopwords_remover import remove_stopwords


def get_topics_bert(sentences: list[str], patient_id=None):
    """
    Function which performs topic detection on given text with BERTopic.
    Hint: in order to perform topic detection with BERTopic our dataset must contain at leas 10 entries.
    """
    umap_model = UMAP(n_neighbors=5,
                      n_components=2,
                      min_dist=0.0,
                      metric='cosine')

    model = BERTopic(umap_model=umap_model,
                     language="multilingual",
                     calculate_probabilities=True)

    topics, probabilities = model.fit_transform(sentences)

    # if a concrete patient ID was given (instead of just the data) visualize results
    if patient_id is not None:
        save_topic_word_scores(model, patient_id)

    print(model.get_topic_info())

    return topics


def save_topic_word_scores(bertopic_model: BERTopic, patient_id: int):
    """
    Function to visualize results of topic modelling performed by BERTopic.
    Saves results as .html file in given path.
    """

    fig = bertopic_model.visualize_barchart()
    file_name = f"/bertopic-patient_{patient_id}.html"
    fig.write_html(config_instance.bertopic_location + file_name)


if __name__ == '__main__':
    example_patient_id = 13

    # get data
    data = db_handler.get_patient_journal_entries(example_patient_id)
    data = [entry.text_entry for entry in data]

    # preprocess data
    data = clean_sentences(data)
    data = [emojis_to_description(entry) for entry in data]
    data = remove_stopwords(data)
    data = lemmatize(data)

    print(get_topics_bert(data))
