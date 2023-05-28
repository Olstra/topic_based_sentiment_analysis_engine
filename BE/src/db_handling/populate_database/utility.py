from BE.src.DTOs.journalEntryDTO import JournalEntryDTO
from BE.src.db_handling.db_handler import db_handler


DELIMITER = "###"


def get_entries_per_date(patient_id: int) -> list[JournalEntryDTO]:
    """
    Consolidate all text entries for a single day into a single data row.
    """
    patient_entries = db_handler.get_patient_journal_entries(patient_id)
    entries_per_date = {}

    for entry in patient_entries:
        if entry.date_written in entries_per_date:
            entries_per_date[entry.date_written] += DELIMITER + entry.text_entry
        else:
            entries_per_date[entry.date_written] = entry.text_entry

    # convert into list of DTOs
    result = []
    for date, text in entries_per_date.items():
        new = JournalEntryDTO(
            patient_id=patient_id,
            date_written=date,
            text_entry=text
        )
        result.append(new)

    return result


if __name__ == '__main__':
    example_patient_id = 3
    print(get_entries_per_date(example_patient_id))
