"""
Load conversation data from given path.
"""
import csv
from datetime import datetime
from typing import List

from BE.src.DTOs.journalEntryDTO import JournalEntryDTO
from BE.src.config import config_instance
from BE.src.db_handling.db_handler import db_handler


def parse_file_lines(filepath: str) -> List[JournalEntryDTO]:
    """
    Read the content of a given file.
    Return the content of that file in the correct DTO representation.
    """
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file, fieldnames=['note', 'id', 'date', 'consultationId', 'patientId', 'accessKey'])
            next(reader)
            result = []
            for row in reader:
                entry_dto = JournalEntryDTO(
                    original_entry_id=row['id'],
                    consultation_id=row['consultationId'],
                    patient_id=db_handler.get_patient_through_original_id(row['patientId']).id,
                    date_written=datetime.strptime(row['date'], '%Y-%m-%d'),
                    text_entry=row['note']
                )
                result.append(entry_dto)
            return result

    except FileNotFoundError:
        raise FileNotFoundError(f"ERROR: The file at {filepath} was not found.")

    except UnicodeDecodeError:
        raise ValueError(f"ERROR: The file at {filepath} is corrupted or not a text file.")


def parse_access_key(key: str) -> int:
    result = key.replace("p", "")
    print("string: ", key)
    return int(result)


if __name__ == '__main__':
    output = parse_file_lines(config_instance.raw_data_path)
    print(output)
