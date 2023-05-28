from dataclasses import dataclass
from sqlite3 import Date
from typing import Optional


@dataclass
class SummaryDTO:
    text_entry: str
    date_written: Date
    patient_id: int
    id: Optional[int] = None
