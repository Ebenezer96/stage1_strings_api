from pydantic import BaseModel
from datetime import datetime
import hashlib

class StringRequest(BaseModel):
    value: str

class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: dict

class StringResponse(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: datetime


def analyze_string(value: str) -> StringProperties:
    cleaned_value = value.lower().replace(" ", "")
    is_palindrome = cleaned_value == cleaned_value[::-1]
    sha256_hash = hashlib.sha256(value.encode()).hexdigest()
    char_freq = {ch: value.count(ch) for ch in set(value)}

    return StringProperties(
        length=len(value),
        is_palindrome=is_palindrome,
        unique_characters=len(set(value)),
        word_count=len(value.split()),
        sha256_hash=sha256_hash,
        character_frequency_map=char_freq
    )
