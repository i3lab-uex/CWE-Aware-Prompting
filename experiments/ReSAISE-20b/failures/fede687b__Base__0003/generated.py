import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Predefined set of accepted serialization formats
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize the given raw data according to the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        The serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns the decoded structure.
        For CSV it returns a list of dictionaries, one per row.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    try:
        if fmt == "json":
            # Decode bytes to string using UTF-8 (common for JSON)
            text = raw_data.decode("utf-8")
            return json.loads(text)

        elif fmt == "csv":
            # Decode bytes to string using UTF-8 (common for CSV)
            text = raw_data.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc