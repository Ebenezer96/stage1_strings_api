from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from models import StringRequest, StringResponse, analyze_string

app = FastAPI(title="String Analyzer API")

# Simple in-memory storage
database = {}

@app.post("/strings", response_model=StringResponse, status_code=status.HTTP_201_CREATED)
def create_string(data: StringRequest):
    if data.value in database:
        raise HTTPException(status_code=409, detail="String already exists")

    properties = analyze_string(data.value)
    response = StringResponse(
        id=properties.sha256_hash,
        value=data.value,
        properties=properties,
        created_at=datetime.utcnow()
    )
    database[data.value] = response
    return response


@app.get("/strings/{string_value}", response_model=StringResponse)
def get_string(string_value: str):
    if string_value not in database:
        raise HTTPException(status_code=404, detail="String not found")
    return database[string_value]


@app.get("/")
def root():
    return {"message": "String Analyzer API running successfully!"}
