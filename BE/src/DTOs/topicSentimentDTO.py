from dataclasses import dataclass
from sqlite3 import Date
from typing import Optional, Dict, List


@dataclass
class TopicSentimentDTO:
    topic: str
    sentiment: float
    journal_entry_id: Optional[str] = None
    patient_id: Optional[int] = None
    date_noted: Optional[Date] = None
    nr_of_occurrences: Optional[int] = None
    id: Optional[int] = None


@dataclass
class AvgTopicSentimentDTO:
    patient_id: int
    topic: str
    overall_sentiment: str
    nr_of_occurrences: int


@dataclass
class ValenceDataPointDTO:
    sentiment_score: float
    date: Date


@dataclass
class ValenceChartDataDTO:
    patient_id: int
    topic: str
    data: List[ValenceDataPointDTO]
