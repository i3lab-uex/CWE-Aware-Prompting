import json
import csv
from io import StringIO
from typing import Any


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize `byte_data` according to the specified serialization method.

    Supported methods (case-insensitive):
        - 'json': JSON format, decoded using UTF-8.
        - 'csv' : CSV format, interpreted as a list of dictionaries.

    Any other method will raise ValueError to prevent unsafe deserialization.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    method = method_of_serialization.strip().lower()

    if method == "json":
        # Decode bytes to string using UTF-8, then parse JSON
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == "csv":
        # Decode bytes to string and parse as CSV
        try:
            text = byte_data.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid CSV data: {exc}") from exc

    # Unsupported or potentially dangerous serialization methods
    raise ValueError(f"Unsupported serialization method: {method_of_serialization}")