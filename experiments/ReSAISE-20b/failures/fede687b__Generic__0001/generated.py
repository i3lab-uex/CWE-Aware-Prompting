import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Define the set of safe serialization formats we allow.
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize the given raw data according to the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        The serialization format used ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON this is whatever the
        underlying JSON structure represents (dict, list, etc.).
        For CSV this is a list of dictionaries where keys are the
        column names.

    Raises
    ------
    ValueError
        If an unsupported or insecure serialization method is used.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    # Decode bytes to text using UTF-8 (common for JSON and CSV)
    try:
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8") from exc

    if fmt == "json":
        # Use json.loads; it does not execute code and is safe for plain data.
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # Read CSV into a list of dictionaries.
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # The code path should never reach here because of the earlier check,
    # but we keep it for completeness.
    raise ValueError(f"Unhandled format: {format_type}")