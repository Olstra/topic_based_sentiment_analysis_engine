from unittest import TestCase

from BE.src.DTOs.moodScoresDTO import MoodScoresDTO
from BE.src.DTOs.summaryDTO import SummaryDTO
from BE.src.analysis.openai_model.openai_model import OpenaiModel
from BE.src.db_handling.db_handler import db_handler


class IntegrationTest(TestCase):
    # Test patient information
    test_patient_id = 1

    def test_whole_process(self):
        # get test patient
        patient = db_handler.get_patient(self.test_patient_id)

        # fetch patient data
        data = db_handler.get_patient_journal_entries(self.test_patient_id)
        data_text = [entry.text_entry for entry in data]

        # analysis #
        model = OpenaiModel()

        # get text summary
        summarized_text = model.summarize_text_to_text(data_text[0], patient.gender)

        # insert text into db
        summary = SummaryDTO(
            patient_id=self.test_patient_id,
            text_entry=summarized_text,
            date_written=data[0].date_written
        )
        db_handler.insert_text_summary(summary)

        # get JSON format out of text
        json_repr = model.summarize_text_to_json(data_text[0])

        moods_dto = MoodScoresDTO(
            overall_motivation=json_repr["overall_motivation"],
            perceived_importance=json_repr["perceived_importance"],
            chance_of_succ=json_repr["chance_of_succ"],
            perceived_control=json_repr["perceived_control"],
            meaningfulness=json_repr["meaningfulness"],
            patient_id=self.test_patient_id,
            date_noted=data[0].date_written
        )

        db_handler.insert_motivation_scores(moods_dto)
