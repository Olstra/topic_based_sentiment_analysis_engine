from dataclasses import dataclass


@dataclass
class EmojiDTO:
    emoji: str  # Unicode representation
    polarity: float
    text_representation: str
