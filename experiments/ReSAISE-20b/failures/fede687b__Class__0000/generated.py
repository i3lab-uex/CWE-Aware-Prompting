import json
import csv
from io import BytesIO
from typing import Any, List, Dict

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize the given byte stream into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The serialized input data.
    format_type : str
        The serialization format used ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it can be any valid
        JSON type (dict, list, str, int, float, bool, None). For CSV it
        returns a list of dictionaries representing rows.

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
            # json.loads expects a string, so decode the bytes safely.
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "csv":
            # Use a BytesIO buffer to read CSV data.
            with BytesIO(raw_data) as buf:
                reader = csv.DictReader(
                    (line.decode("utf-8") for line in buf),
                    delimiter=",",
                )
                return [row for row in reader]
    except Exception as exc:
        # Wrap any exception to avoid leaking internal details.
        raise ValueError(f"Failed to deserialize data: {exc}") from None