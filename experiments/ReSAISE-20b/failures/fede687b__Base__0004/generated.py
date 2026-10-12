import json
import csv
from io import BytesIO
from typing import Any, List, Dict


# Whitelist of safe serialization formats
ALLOWED_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize raw binary data into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        Serialization format used. Must be one of the values in ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a native Python structure.
        For CSV, a list of dictionaries (each row as a dict).

    Raises
    ------
    ValueError
        If the format_type is unsupported or if deserialization fails.
    """
    if not isinstance(raw_data, bytes):
        raise ValueError("raw_data must be of type 'bytes'")

    format_type = format_type.lower()
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization method: '{format_type}'")

    try:
        if format_type == "json":
            # Decode bytes to string and parse JSON
            text = raw_data.decode("utf-8")
            return json.loads(text)

        if format_type == "csv":
            # Parse CSV into list of dictionaries
            with BytesIO(raw_data) as bio:
                text_stream = io.TextIOWrapper(bio, encoding="utf-8", newline="")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]

    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc
    except csv.Error as exc:
        raise ValueError(f"Failed to deserialize CSV data: {exc}") from exc

    # This point should never be reached because all allowed formats are handled above
    raise ValueError(f"Unhandled format_type: {format_type}")