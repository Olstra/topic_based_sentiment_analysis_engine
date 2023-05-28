from dataclasses import dataclass
from sqlite3 import Date
from typing import Optional


@dataclass
class JournalEntryDTO:
    text_entry: str
    date_written: Date
    patient_id: int
    original_entry_id: Optional[str] = None
    consultation_id: Optional[str] = None
    id: Optional[int] = None
