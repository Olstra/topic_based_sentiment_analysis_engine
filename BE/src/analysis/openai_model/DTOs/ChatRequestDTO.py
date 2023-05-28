from dataclasses import dataclass

from typing import List, Dict


@dataclass
class ChatRequestDTO:
    model: str
    messages: List[Dict[str, str]]
    temperature: float
