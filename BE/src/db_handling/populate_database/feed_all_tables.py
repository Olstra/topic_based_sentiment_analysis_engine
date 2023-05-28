from BE.src.db_handling.db_handler import db_handler
from BE.src.db_handling.populate_database.feed_journal_entries import feed_journal_entries_to_db
from BE.src.db_handling.populate_database.feed_motivation_scores import feed_motivation_scores
from BE.src.db_handling.populate_database.feed_patients import feed_patients
from BE.src.db_handling.populate_database.feed_summaries import feed_summaries_to_db
from BE.src.db_handling.populate_database.feed_topic_sentiments import feed_topic_sentiments
from BE.src.db_handling.populate_database.feed_valence import feed_valence_activities


def populate_db(patient_id=None) -> None:
    """
    Populate or update engine database.
    If no patient id was provided we will run this process for all patients in the database.
    """
    feed_patients()
    feed_journal_entries_to_db()

    if patient_id is not None:
        feed_topic_sentiments(patient_id)
        feed_summaries_to_db(patient_id)
        feed_motivation_scores(patient_id)
        feed_valence_activities(patient_id)
    else:
        all_patients_ids = db_handler.get_all_patient_ids()

        for current_patient_id in all_patients_ids:
            feed_topic_sentiments(current_patient_id)
            feed_summaries_to_db(current_patient_id)
            feed_motivation_scores(current_patient_id)
            feed_valence_activities(current_patient_id)


if __name__ == '__main__':
    example_patient_id = 90
    populate_db()
