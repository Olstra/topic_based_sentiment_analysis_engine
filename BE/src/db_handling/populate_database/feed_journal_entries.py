"""
This is a helper function that populates the database with journal entries for all patients.
The journal entries are sourced from the './Data' directory and are read in accordance with the path specified in the .env file.
"""
from BE.src.config import config_instance
from BE.src.preprocessing.data_loader import parse_file_lines
from BE.src.db_handling.db_handler import DbHandler, db_handler


def feed_journal_entries_to_db():
    parsed_data = parse_file_lines(config_instance.raw_data_path)

    for journal_entry in parsed_data:
        if db_handler.get_journal_entry_through_original_id(journal_entry.original_entry_id) is None:
            db_handler.insert_journal_entry(journal_entry)


if __name__ == '__main__':
    feed_journal_entries_to_db()
