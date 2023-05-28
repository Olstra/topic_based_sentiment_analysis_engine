from sqlite3 import Date
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class MoodScoresDTO:
    date_noted: Date
    patient_id: int
    overall_motivation: float
    perceived_importance: int
    chance_of_succ: int
    perceived_control: int
    meaningfulness: int
    id: Optional[int] = None
    journal_entry_id:  Optional[int] = None
