"""
Helper function to fill database with the values of the patients motivation scores.
"""
import time

from BE.src.DTOs.moodScoresDTO import MoodScoresDTO
from BE.src.analysis.openai_model import openai_model
from BE.src.db_handling.db_handler import db_handler


def feed_motivation_scores(patient_id: int) -> None:
    """
    Calculate motivation scores for a certain patient through the model & fill in results in db.
    """
    model = openai_model.OpenaiModel()
    patient_entries = db_handler.get_patient_journal_entries(patient_id)

    for entry in patient_entries:
        answer = model.summarize_text_to_json(entry.text_entry)
        mood_repr = MoodScoresDTO(
            overall_motivation=answer.get("overall_motivation", None),
            perceived_importance=answer.get("perceived_importance", None),
            chance_of_succ=answer.get("chance_of_succ", None),
            perceived_control=answer.get("perceived_control", None),
            meaningfulness=answer.get("meaningfulness", None),
            patient_id=entry.patient_id,
            date_noted=entry.date_written,
            journal_entry_id=entry.id

        )
        db_handler.insert_motivation_scores(mood_repr)

        # wait 20s due to ChatGPT restriction to 3 requests per minute
        print("Waiting 20 seconds...")
        time.sleep(20)


if __name__ == '__main__':
    example_patient_id = 99
    feed_motivation_scores(example_patient_id)
