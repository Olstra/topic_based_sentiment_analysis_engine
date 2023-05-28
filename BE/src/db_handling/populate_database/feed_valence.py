"""
Helper function to fill database with the values of the patients motivation scores.
"""
import time

from BE.src.DTOs.topicSentimentDTO import TopicSentimentDTO
from BE.src.analysis.openai_model import openai_model
from BE.src.db_handling.db_handler import DbHandler


def feed_valence_activities(patient_id: int) -> None:
    """
    Compute the legacy_wordcloud score for each activity of a specific patient using the established model, and persist the
    results in the database.
    """
    db_handler = DbHandler()
    model = openai_model.OpenaiModel()
    patient_entries = db_handler.get_patient_journal_entries(patient_id)

    for e in patient_entries:
        answer = model.get_valence_activities(e.text_entry)
        if answer != {}:
            for activity in answer["legacy_wordcloud"]:
                entry_dto = TopicSentimentDTO(
                    patient_id=patient_id,
                    topic=activity["topic"],
                    sentiment=activity["sentiment"],
                    date_noted=e.date_written
                )
                db_handler.insert_valence_activity(entry_dto)

        # wait 20s due to ChatGPT restriction to 3 requests per minute
        print("Waiting 20 seconds...")
        time.sleep(20)


if __name__ == '__main__':
    example_patient_id = 1
    feed_valence_activities(example_patient_id)
