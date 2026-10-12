import json
import csv
from io import StringIO
from typing import Any, List, Dict


# Define the set of serialization formats that are considered safe
ALLOWED_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize the given byte stream into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    format_type : str
        The serialization format used (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.  For JSON it will be a dict/list/etc.
        For CSV it will be a list of dictionaries (each row as a dict).

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS or if the data cannot be parsed.
    """
    # Normalise format string
    fmt = format_type.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_type}'")

    try:
        if fmt == "json":
            # json.loads expects a string; decode bytes to UTF-8
            return json.loads(raw_data.decode("utf-8"))

        if fmt == "csv":
            # CSV is decoded to a text stream and read via csv.DictReader
            text = raw_data.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            # Convert to list of dicts
            return [row for row in reader]

    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
        # Wrap parsing errors in ValueError to keep the API consistent
        raise ValueError(f"Failed to deserialize data: {exc}") from exc