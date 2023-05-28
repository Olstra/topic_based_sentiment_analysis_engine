import logging
import sqlite3
from typing import Optional

import BE.src.db_handling.constants.table_names as table_names
from BE.src.DTOs.journalEntryDTO import JournalEntryDTO
from BE.src.DTOs.moodScoresDTO import MoodScoresDTO
from BE.src.DTOs.patientDTO import PatientDTO
from BE.src.DTOs.summaryDTO import SummaryDTO
from BE.src.DTOs.topicSentimentDTO import TopicSentimentDTO
from BE.src.config import config_instance
from BE.src.db_handling.constants.schemas import PATIENT_SCHEMA, JOURNAL_ENTRY_SCHEMA, SUMMARY_SCHEMA, \
    MOTIVATION_SCORES_SCHEMA, VALENCE_SCHEMA

logging.basicConfig(level=logging.INFO)


class DbHandler:
    """
    The 'DbHandler' class manages SQLite database interactions for the engine, including table setup with corresponding
    schemas, as well as adding, deleting, and retrieving information from the database.
    """
    def __init__(self):
        self.conn = sqlite3.connect(config_instance.db_location)
        self.cursor = self.conn.cursor()

        self._create_tables_if_not_exist()

        logging.info("Successfully established connection to database.")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def _create_tables_if_not_exist(self):
        self._create_table(table_names.PATIENTS, PATIENT_SCHEMA)
        self._create_table(table_names.JOURNAL_ENTRIES, JOURNAL_ENTRY_SCHEMA)
        self._create_table(table_names.SUMMARIES, SUMMARY_SCHEMA)
        self._create_table(table_names.MOTIVATION_SCORES, MOTIVATION_SCORES_SCHEMA)
        self._create_table(table_names.VALENCE, VALENCE_SCHEMA)
        self._create_table(table_names.TOPIC_SENTIMENTS, VALENCE_SCHEMA)

        self.conn.commit()

    def _create_table(self, table_name, table_schema):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({table_schema})')

    def insert_patient(self, patient: PatientDTO):
        query = f'INSERT INTO {table_names.PATIENTS} (forename, lastname, gender, original_id) VALUES (?, ?, ?, ?)'
        values = (patient.forename, patient.lastname, patient.gender, patient.original_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_valence_activity(self, entry: TopicSentimentDTO):
        query = f'INSERT INTO {table_names.VALENCE} (patient_id, topic, sentiment, date_noted) VALUES (?, ?, ?, ?)'
        values = (entry.patient_id, entry.topic, entry.sentiment, entry.date_noted)
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_topic_sentiment(self, entry: TopicSentimentDTO):
        query = f'INSERT INTO {table_names.TOPIC_SENTIMENTS} (patient_id, topic, sentiment, date_noted, journal_entry_id) VALUES (?, ?, ?, ?, ?)'
        values = (entry.patient_id, entry.topic, entry.sentiment, entry.date_noted, entry.journal_entry_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_text_summary(self, entry: SummaryDTO):
        query = f'INSERT INTO {table_names.SUMMARIES} (patient_id, text_entry, timestamp_written) VALUES (?, ?, ?)'
        values = (entry.patient_id, entry.text_entry, entry.date_written)
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_journal_entry(self, entry: JournalEntryDTO):
        query = f'INSERT INTO {table_names.JOURNAL_ENTRIES} (original_id, patient_id, text_entry, date_written, consultation_id) VALUES (?, ?, ?, ?, ?)'
        values = (entry.original_entry_id, entry.patient_id, entry.text_entry, entry.date_written, entry.consultation_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_motivation_scores(self, scores: MoodScoresDTO):
        query = (
            f"INSERT INTO {table_names.MOTIVATION_SCORES} "
            "(date_noted, patient_id, journal_entry_id, overall_motivation, "
            "perceived_importance, chance_of_succ, perceived_control, meaningfulness) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        values = (
            scores.date_noted, scores.patient_id, scores.journal_entry_id,
            scores.overall_motivation, scores.perceived_importance, scores.chance_of_succ,
            scores.perceived_control, scores.meaningfulness
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_patient(self, given_patient_id):
        query = f"DELETE FROM {table_names.PATIENTS} WHERE id = ?"
        self.cursor.execute(query, (str(given_patient_id),))
        self.conn.commit()

    def delete_text(self, text):
        query = f"DELETE FROM {table_names.SUMMARIES} WHERE text_entry = ?"
        self.cursor.execute(query, (text,))
        self.conn.commit()

    def get_patient_id(self, forename, lastname) -> Optional[int]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f"SELECT id FROM {table_names.PATIENTS} WHERE forename=? AND lastname=?"
        cursor.execute(query, (forename, lastname))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_all_patient_ids(self) -> list[int]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f"SELECT id FROM {table_names.PATIENTS}"
        cursor.execute(query)
        results = cursor.fetchall()
        return [result[0] for result in results]

    def get_all_journal_entries(self) -> list[JournalEntryDTO]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_names.JOURNAL_ENTRIES}"
        cursor.execute(query)
        result = cursor.fetchall()
        entries = [
            JournalEntryDTO(
                patient_id=e[4],
                text_entry=e[1],
                date_written=e[2],
                consultation_id=e[3]
            ) for e in result
        ]
        return entries

    def get_patient_journal_entries(self, patient_id: int) -> list[JournalEntryDTO]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_names.JOURNAL_ENTRIES} WHERE patient_id=?"
        cursor.execute(query, (str(patient_id),))
        result = cursor.fetchall()
        entries = [
            JournalEntryDTO(
                id=e[0],
                text_entry=e[1],
                date_written=e[2],
                consultation_id=e[3],
                original_entry_id=e[4],
                patient_id=e[5]
            ) for e in result
        ]
        return entries

    def get_patient_summaries(self, patient_id: int) -> list[SummaryDTO]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_names.SUMMARIES} WHERE patient_id=?"
        cursor.execute(query, (patient_id,))
        result = cursor.fetchall()
        entries = [
            SummaryDTO(
                patient_id=e[3],
                text_entry=e[1],
                date_written=e[2]
            ) for e in result
        ]
        return entries

    def get_patient_mood_scores(self, patient_id):
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_names.MOTIVATION_SCORES} WHERE patient_id=?"
        cursor.execute(query, (patient_id,))
        result = cursor.fetchall()
        entries = [
            MoodScoresDTO(
                date_noted=e[1],
                patient_id=e[2],
                overall_motivation=e[3],
                perceived_importance=e[4],
                chance_of_succ=e[5],
                perceived_control=e[6],
                meaningfulness=e[7],
                id=e[0],
                journal_entry_id=e[8]
            ) for e in result
        ]
        return entries

    def get_patient(self, patient_id: int) -> Optional[PatientDTO]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f'SELECT * FROM {table_names.PATIENTS} WHERE id=?'
        cursor.execute(query, (str(patient_id),))
        result = cursor.fetchone()
        if result:
            return PatientDTO(
                id=result[0],
                forename=result[1],
                lastname=result[2],
                gender=result[3],
                original_id=result[4]
            )
        else:
            return None

    def get_patient_through_original_id(self, original_id: str) -> Optional[PatientDTO]:
        """
        In the provided dataset each patient already had an ID. But for easier testing we assign each patient a new ID
        in our application. This function returns the ID the patient had in the original dataset.
        """
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f'SELECT * FROM {table_names.PATIENTS} WHERE original_id=?'
        cursor.execute(query, (original_id,))
        result = cursor.fetchone()
        if result:
            return PatientDTO(
                id=result[0],
                forename=result[1],
                lastname=result[2],
                gender=result[3],
                original_id=result[4]
            )
        else:
            return None

    def get_journal_entry_through_original_id(self, original_id: str) -> Optional[JournalEntryDTO]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f'SELECT * FROM {table_names.JOURNAL_ENTRIES} WHERE original_id=?'
        cursor.execute(query, (original_id,))
        result = cursor.fetchone()
        if result:
            return JournalEntryDTO(
                id=result[0],
                text_entry=result[1],
                date_written=result[2],
                consultation_id=result[3],
                original_entry_id=result[4],
                patient_id=result[5]
            )
        else:
            return None

    def get_patient_topics_sentiments(self, patient_id: int) -> list[TopicSentimentDTO]:
        conn = sqlite3.connect(config_instance.db_location)
        cursor = conn.cursor()
        query = f'SELECT * FROM {table_names.TOPIC_SENTIMENTS} WHERE patient_id=?'
        cursor.execute(query, (patient_id,))
        result = cursor.fetchall()
        print("result: ", result)
        entries = [TopicSentimentDTO(
            id=e[0],
            patient_id=e[1],
            topic=e[2],
            sentiment=e[3],
            date_noted=e[4]
        ) for e in result]
        return entries


db_handler = DbHandler()


if __name__ == '__main__':
    test_db_handler = DbHandler()
    example_patient_id = 1
    print(test_db_handler.get_patient_summaries(example_patient_id))
