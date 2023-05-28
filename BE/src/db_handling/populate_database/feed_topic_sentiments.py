"""
Helper function to fill database with the values of the patients detected topics and according sentiments.
"""
import time

from BE.src.analysis.topic_based_sentiment_analyzer import topic_based_sentiment_analysis
from BE.src.db_handling.db_handler import db_handler
from BE.src.db_handling.populate_database.utility import get_entries_per_date, DELIMITER


def feed_topic_sentiments(patient_id: int) -> None:
    #data = get_entries_per_date(patient_id)
    data = db_handler.get_patient_summaries(patient_id)

    for entry in data:
        #text = entry.text_entry.split(DELIMITER)
        #for sentence in text:
        result = topic_based_sentiment_analysis(entry.text_entry)
        for r in result:
            r.patient_id = patient_id
            r.date_noted = entry.date_written
            r.journal_entry_id = entry.id
            db_handler.insert_topic_sentiment(r)


if __name__ == '__main__':
    example_patient_id = 12
    feed_topic_sentiments(example_patient_id)
