from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from hashlib import sha256
from datetime import datetime

app = FastAPI(title="String Analyzer Service")

# in-memory database
db = {}


class StringRequest(BaseModel):
    value: str


def analyze_string(value: str):
    value_clean = value.strip()
    properties = {
        "length": len(value_clean),
        "is_palindrome": value_clean.lower() == value_clean[::-1].lower(),
        "unique_characters": len(set(value_clean)),
        "word_count": len(value_clean.split()),
        "sha256_hash": sha256(value_clean.encode()).hexdigest(),
        "character_frequency_map": {ch: value_clean.count(ch) for ch in set(value_clean)}
    }
    return properties


@app.post("/strings", status_code=201)
def create_string(request: StringRequest):
    if not isinstance(request.value, str):
        raise HTTPException(status_code=422, detail="Value must be a string")

    string_value = request.value.strip()
    if not string_value:
        raise HTTPException(status_code=400, detail="Missing or empty value")

    properties = analyze_string(string_value)
    string_id = properties["sha256_hash"]

    if string_id in db:
        raise HTTPException(status_code=409, detail="String already exists")

    db[string_id] = {
        "id": string_id,
        "value": string_value,
        "properties": properties,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    return db[string_id]


@app.get("/strings/{string_value}")
def get_string(string_value: str):
    for record in db.values():
        if record["value"] == string_value:
            return record
    raise HTTPException(status_code=404, detail="String not found")


@app.get("/strings")
def get_all_strings(
    is_palindrome: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    word_count: int | None = None,
    contains_character: str | None = None,
):
    results = list(db.values())

    if is_palindrome is not None:
        results = [s for s in results if s["properties"]["is_palindrome"] == is_palindrome]
    if min_length is not None:
        results = [s for s in results if s["properties"]["length"] >= min_length]
    if max_length is not None:
        results = [s for s in results if s["properties"]["length"] <= max_length]
    if word_count is not None:
        results = [s for s in results if s["properties"]["word_count"] == word_count]
    if contains_character is not None:
        results = [s for s in results if contains_character in s["value"]]

    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character,
    }

    return {"data": results, "count": len(results), "filters_applied": filters}


@app.get("/strings/filter-by-natural-language")
def natural_language_filter(query: str = Query(...)):
    parsed = {}
    q = query.lower()

    if "palindromic" in q:
        parsed["is_palindrome"] = True
    if "single word" in q:
        parsed["word_count"] = 1
    if "longer than" in q:
        try:
            num = int(q.split("longer than")[1].split()[0])
            parsed["min_length"] = num + 1
        except:
            pass
    if "containing the letter" in q:
        try:
            ch = q.split("letter")[1].strip().split()[0]
            parsed["contains_character"] = ch
        except:
            pass

    if not parsed:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    results = get_all_strings(**parsed)["data"]
    return {"data": results, "count": len(results), "interpreted_query": {"original": query, "parsed_filters": parsed}}


@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    for key, record in list(db.items()):
        if record["value"] == string_value:
            del db[key]
            return
    raise HTTPException(status_code=404, detail="String not found")
