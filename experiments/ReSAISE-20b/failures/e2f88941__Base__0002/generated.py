import json
import csv
import io
from typing import Any, List, Dict

# Define the set of serialization methods that are considered safe.
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe methods.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data as a byte string.
    format_method : str
        Identifier of the serialization method used ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it can be any native type.
        For CSV the result is a list of dictionaries mapping column names to values.

    Raises
    ------
    ValueError
        If the provided format_method is not in SAFE_METHODS.
    """
    method = format_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or unrecognized.")

    # JSON deserialization
    if method == "json":
        try:
            text = data_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data.") from exc

    # CSV deserialization
    if method == "csv":
        try:
            text = data_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV data.") from exc

    # The following line is unreachable due to the earlier check,
    # but it keeps type-checkers happy.
    raise ValueError(f"Unsupported format method: {format_method}")