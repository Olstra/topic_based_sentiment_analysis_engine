from unittest import TestCase

from BE.src.DTOs.moodScoresDTO import MoodScoresDTO
from BE.src.DTOs.topicSentimentDTO import ValenceActivityDTO
from BE.src.analysis.openai_model import openai_model
from BE.src.db_handling.db_handler import DbHandler


class OpenAiModelTest(TestCase):

    db_handler = DbHandler()
    model = openai_model.OpenaiModel()
   # parsed_data = read_file_lines(config_instance.raw_data_path)

    test_patient_id = 1

    def test_feed_summaries_to_db(self):
        # get test patient
        test_patient = self.db_handler.get_patient(self.test_patient_id)

        # parse raw data files
        for journal_entry in self.parsed_data:
            text_summary = self.model.summarize_text_to_text(journal_entry.text_entry, test_patient.gender)
            self.db_handler.insert_text_summary(
                patient_id=journal_entry.patient_id,
                content=text_summary,
                timestamp=journal_entry.date_written
            )

    def test_fill_in_motivation_scores(self):
        pass

    def test_valence(self):
        pass
