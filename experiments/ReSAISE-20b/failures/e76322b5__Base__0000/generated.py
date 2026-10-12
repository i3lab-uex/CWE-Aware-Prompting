import json
import csv
from io import StringIO
from typing import Any, List, Dict


# Set of serialization formats that are considered safe for untrusted input
ALLOWED_FORMATS = {"json", "csv"}


def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize input data from a given serialization format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data.
    format_name : str
        Name of the serialization format ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    try:
        if fmt == "json":
            # JSON expects text, so decode bytes to str
            decoded_text = encoded_bytes.decode("utf-8")
            return json.loads(decoded_text)

        elif fmt == "csv":
            # CSV is read from text; decode bytes and use csv.DictReader
            decoded_text = encoded_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(decoded_text))
            # Return a list of dictionaries
            return [row for row in reader]

    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
        raise ValueError(f"Failed to deserialize data using format '{format_name}': {exc}") from exc