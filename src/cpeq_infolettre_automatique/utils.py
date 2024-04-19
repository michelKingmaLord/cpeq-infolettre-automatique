"""Utility functions for processing and saving data."""
import json


def process_raw_response(raw_response: str) -> list:
    """Converts raw JSON lines into a list of dictionaries (valid JSON array)."""
    try:
        data = [json.loads(line) for line in raw_response.strip().split("\n") if line.strip()]
    except json.JSONDecodeError as error:
        return {"error": "Failed to decode JSON", "details": str(error)}
    else:
        return data


def save_data_to_json(data: list, file_path: str ="output.json") -> str:
    """Saves processed data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return f"Data successfully saved to {file_path}"
    except IOError as error:
        return {"error": "Failed to write to file", "details": str(error)}
