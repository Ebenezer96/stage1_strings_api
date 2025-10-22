# String Analyzer API: Dynamic String Property Insights ✨

## Overview
This project is a high-performance Python FastAPI backend that processes and analyzes string data, providing insights into various properties such as length, palindrome status, unique characters, word count, SHA256 hash, and character frequency. It utilizes an in-memory dictionary for efficient data storage and retrieval, with an underlying SQLAlchemy setup poised for future database integration.

## Features
- **Comprehensive String Analysis**: Automatically computes six key properties for any submitted string: length, palindrome status, unique character count, word count, SHA256 hash, and character frequency map.
- **RESTful API**: Exposes intuitive endpoints for submitting new strings for analysis and retrieving previously analyzed string data.
- **Duplicate String Prevention**: Ensures data integrity by rejecting submission of strings that have already been processed and stored.
- **Efficient In-Memory Storage**: Leverages a simple in-memory dictionary for rapid storage and retrieval of string analysis results, ideal for quick demonstrations and caching.
- **Scalability Ready**: Includes a SQLAlchemy configuration, allowing for seamless transition to persistent database storage (e.g., SQLite, PostgreSQL) as the project scales.
- **Built with FastAPI**: Benefits from FastAPI's high performance, automatic interactive API documentation (Swagger UI), and robust data validation powered by Pydantic.

## Technologies Used

| Technology    | Description                                       | Link                                                       |
| :------------ | :------------------------------------------------ | :--------------------------------------------------------- |
| Python        | Primary programming language.                     | [Python.org](https://www.python.org/)                      |
| FastAPI       | High-performance web framework for building APIs. | [FastAPI.tiangolo.com](https://fastapi.tiangolo.com/)      |
| Pydantic      | Data validation and settings management.          | [Pydantic-docs.helpmanual.io](https://pydantic-docs.helpmanual.io/) |
| Uvicorn       | ASGI server for running FastAPI applications.     | [Uvicorn.org](https://www.uvicorn.org/)                    |
| SQLAlchemy    | SQL toolkit and Object-Relational Mapper (ORM).   | [SQLAlchemy.org](https://www.sqlalchemy.org/)              |

## Getting Started

Follow these steps to get the String Analyzer API up and running on your local machine.

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd stage1_strings_api
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    -   **On macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```
    -   **On Windows**:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install Dependencies**:
    Install all required packages using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

This project currently does not require any environment variables for its core functionality. The SQLite database URL is hardcoded for simplicity in this stage.

## Usage

Once the dependencies are installed and the virtual environment is active, you can start the API server using Uvicorn.

1.  **Run the API Server**:
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables auto-reloading of the server when code changes are detected, which is useful for development.
    The API will be accessible at `http://127.0.0.1:8000` by default.

2.  **Access Interactive API Documentation**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive Swagger UI documentation, where you can test the endpoints directly.

3.  **Example API Interaction (using `curl`)**:

    *   **Health Check**:
        ```bash
        curl http://127.0.0.1:8000/
        ```
        Expected Output:
        ```json
        {"message": "String Analyzer API running successfully!"}
        ```

    *   **Create/Analyze a String**:
        ```bash
        curl -X POST "http://127.0.0.1:8000/strings" \
             -H "Content-Type: application/json" \
             -d '{"value": "madam"}'
        ```
        Expected Output:
        ```json
        {
          "id": "7616f73167f42d20f666b6c698336cf988f572c6947ac00f5c1d1a104085f1c9",
          "value": "madam",
          "properties": {
            "length": 5,
            "is_palindrome": true,
            "unique_characters": 3,
            "word_count": 1,
            "sha256_hash": "7616f73167f42d20f666b6c698336cf988f572c6947ac00f5c1d1a104085f1c9",
            "character_frequency_map": {
              "m": 2,
              "a": 2,
              "d": 1
            }
          },
          "created_at": "2023-10-27T10:00:00.000000"
        }
        ```
        (Note: `created_at` will reflect the current UTC time.)

    *   **Retrieve an Analyzed String**:
        ```bash
        curl http://127.0.0.1:8000/strings/madam
        ```
        Expected Output (same as above):
        ```json
        {
          "id": "7616f73167f42d20f666b6c698336cf988f572c6947ac00f5c1d1a104085f1c9",
          "value": "madam",
          "properties": {
            "length": 5,
            "is_palindrome": true,
            "unique_characters": 3,
            "word_count": 1,
            "sha256_hash": "7616f73167f42d20f666b6c698336cf988f572c6947ac00f5c1d1a104085f1c9",
            "character_frequency_map": {
              "m": 2,
              "a": 2,
              "d": 1
            }
          },
          "created_at": "2023-10-27T10:00:00.000000"
        }
        ```

## API Documentation

### Base URL
`http://127.0.0.1:8000`

### Endpoints

#### `GET /`
Returns a welcome message indicating the API is running.

**Request**:
No request body.

**Response**:
```json
{
  "message": "String Analyzer API running successfully!"
}
```

**Errors**:
None.

#### `POST /strings`
Submits a string for analysis, stores its properties, and returns the detailed analysis.

**Request**:
```json
{
  "value": "string to analyze"
}
```
**Required fields**:
- `value`: (string) The string to be analyzed.

**Response**:
```json
{
  "id": "sha256_hash_of_value",
  "value": "original_string",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 10,
    "word_count": 3,
    "sha256_hash": "sha256_hash_of_value",
    "character_frequency_map": {
      "s": 2,
      "t": 2,
      "r": 1,
      "i": 1,
      "n": 2,
      "g": 1,
      " ": 2,
      "o": 1,
      "a": 2,
      "l": 1,
      "y": 1,
      "z": 1,
      "e": 1
    }
  },
  "created_at": "2023-10-27T10:00:00.000000"
}
```

**Errors**:
- `409 Conflict`: Returned if the submitted string (`value`) already exists in the system.

#### `GET /strings/{string_value}`
Retrieves the analysis and properties of a previously submitted string.

**Request**:
No request body. The string to retrieve is part of the URL path.

**Response**:
```json
{
  "id": "sha256_hash_of_value",
  "value": "original_string",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "sha256_hash": "sha256_hash_of_value",
    "character_frequency_map": {
      "m": 2,
      "a": 2,
      "d": 1
    }
  },
  "created_at": "2023-10-27T10:00:00.000000"
}
```

**Errors**:
- `404 Not Found`: Returned if the `string_value` does not exist in the system.

## Author Info

Connect with me!

-   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/your-username)
-   **Portfolio**: [Your Portfolio Website](https://www.yourportfolio.com)
-   **Twitter**: [Your Twitter Handle](https://twitter.com/your_username)

---

## Badges
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119.1-009688?style=flat&logo=fastapi)
![Pydantic](https://img.shields.io/badge/Pydantic-2.12.3-green?style=flat&logo=pydantic)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.38.0-orange?style=flat&logo=uvicorn)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.44-darkred?style=flat&logo=sqlalchemy)
![GitHub last commit](https://img.shields.io/github/last-commit/EbenezerAmakato/stage1_strings_api)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)