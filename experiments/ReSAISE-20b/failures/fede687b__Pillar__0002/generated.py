import json
import csv
from io import StringIO
from typing import Any, List, Dict


# Define the set of serialization formats that are considered safe
ALLOWED_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize raw binary data into a Python object using the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        The serialization format used. Supported values are 'json' and 'csv'.

    Returns
    -------
    Any
        The deserialized Python object. For JSON this is the parsed value.
        For CSV this returns a list of dictionaries (one per row).

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS or if decoding/parsing fails.
    """
    # Ensure the format is allowed
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_type}'")

    # Decode the raw bytes to a string
    try:
        text = raw_data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to decode raw data as UTF-8") from exc

    # Perform deserialization based on the format
    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # Use StringIO to provide a file-like object for csv.DictReader
        try:
            with StringIO(text) as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to parse CSV data") from exc

    # The code should never reach this point because of the earlier check
    raise ValueError(f"Unhandled format: {format_type}")