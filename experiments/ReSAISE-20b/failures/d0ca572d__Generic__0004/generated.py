import json
import csv
import io
from typing import Any

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    safe serialization methods.

    Parameters:
        data_bytes_stream (bytes): The serialized data as bytes.
        method_of_serialization (str): Identifier of the serialization format
            ('json', 'csv').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the serialization method is not recognized or disallowed.
    """
    # Define safe methods
    _SAFE_METHODS = {
        'json': _deserialize_json,
        'csv':  _deserialize_csv
    }

    method = method_of_serialization.lower()
    if method not in _SAFE_METHODS:
        raise ValueError(f"Disallowed or unknown serialization method: {method}")

    return _SAFE_METHODS[method](data_bytes_stream)


def _deserialize_json(data: bytes) -> Any:
    """
    Safely deserialize JSON data. Assumes UTF‑8 encoding.
    """
    try:
        text = data.decode('utf-8')
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON data") from exc


def _deserialize_csv(data: bytes) -> list[dict[str, str]]:
    """
    Safely deserialize CSV data into a list of dictionaries.
    Assumes UTF‑8 encoding and that the first row contains headers.
    """
    try:
        text_stream = io.StringIO(data.decode('utf-8'))
        reader = csv.DictReader(text_stream)
        return [row for row in reader]
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid CSV encoding") from exc