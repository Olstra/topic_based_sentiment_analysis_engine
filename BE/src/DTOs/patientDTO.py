from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class PatientDTO:
    forename: str
    lastname: str
    gender: str
    original_id: Optional[str] = None
    id: Optional[int] = None
