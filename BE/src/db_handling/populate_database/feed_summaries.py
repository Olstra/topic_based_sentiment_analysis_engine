"""
This is a helper function that populates the database with the summaries of the journal entries for all patients.
"""
import time

from BE.src.DTOs.journalEntryDTO import JournalEntryDTO
from BE.src.DTOs.summaryDTO import SummaryDTO
from BE.src.analysis.openai_model.openai_model import OpenaiModel
from BE.src.db_handling.db_handler import DbHandler
from BE.src.db_handling.populate_database.utility import get_entries_per_date

db_handler = DbHandler()
model = OpenaiModel()


def feed_summaries_to_db(patient_id: int) -> None:
    entries_per_date = get_entries_per_date(patient_id)
    insert_summaries_in_db(entries_per_date, patient_id)


def insert_summaries_in_db(input_lst: list[JournalEntryDTO], patient_id: int):
    for entry in input_lst:
        summary = model.summarize_text_to_text(entry.text_entry, "male")
        summary_dto = SummaryDTO(
            patient_id=patient_id,
            text_entry=summary,
            date_written=entry.date_written
        )
        db_handler.insert_text_summary(summary_dto)

        # wait 20s due to ChatGPT restriction to 3 requests per minute
        print("Waiting 20 seconds...")
        time.sleep(20)


if __name__ == '__main__':
    example_patient_id = 98
    feed_summaries_to_db(example_patient_id)
