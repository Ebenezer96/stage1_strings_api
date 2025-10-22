# schemas.py
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class StringCreate(BaseModel):
    value: str

class Properties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringResponse(BaseModel):
    id: str
    value: str
    properties: Properties
    created_at: datetime

    class Config:
        orm_mode = True
