# utils.py
import hashlib
from collections import Counter
from datetime import datetime, timezone

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def normalized(s: str) -> str:
    # For palindrome checks we consider case-insensitive and consider all characters
    return s.lower()

def compute_properties(s: str) -> dict:
    # Trim? Keep original whitespace; spec doesn't require trimming
    val = s
    length = len(val)
    low = val.lower()
    is_pal = low == low[::-1]
    unique_chars = len(set(val))
    words = val.split()
    wc = len(words)
    sha = sha256_hex(val)
    freq = dict(Counter(val))
    return {
        "length": length,
        "is_palindrome": is_pal,
        "unique_characters": unique_chars,
        "word_count": wc,
        "sha256_hash": sha,
        "character_frequency_map": freq
    }

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
