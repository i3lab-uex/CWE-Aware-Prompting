import json
import csv
import io
from typing import Any

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Safely deserialize `serialized_data` using the specified `deserialization_method`.

    Supported methods:
        - 'json' : Returns a Python object decoded from JSON.
        - 'csv'  : Returns a list of dictionaries, one per CSV row.

    Raises:
        ValueError: If the deserialization method is unsupported or potentially unsafe.
    """
    # Normalize method name
    method = deserialization_method.strip().lower()

    if method == "json":
        # Decode bytes to str and parse JSON
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF‑8 encoded") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Decode bytes to text and parse CSV
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV data must be UTF‑8 encoded") from exc
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # Any other method is considered unsafe or unsupported
    raise ValueError(f"Unsupported deserialization method: {deserialization_method!r}")