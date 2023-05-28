from dataclasses import dataclass


@dataclass
class SentimentDTO:
    polarity: float
    subjectivity: float
    sentence: str
