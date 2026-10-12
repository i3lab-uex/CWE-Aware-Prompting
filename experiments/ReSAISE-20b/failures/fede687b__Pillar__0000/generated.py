import json
import csv
from typing import Any, List, Dict
from io import BytesIO


# ------------------------------------------------------------------
# Accepted serialization formats.  The set deliberately excludes
# insecure/unsafe formats such as pickle or marshal.
ALLOWED_FORMATS = {"json", "csv"}
# ------------------------------------------------------------------


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize *raw_data* according to the specified *format_type*.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        One of the accepted serialization formats ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.  For JSON it can be any JSON
        compatible type (dict, list, str, int, float, bool, None).  For
        CSV it returns a list of dictionaries mapping column names to
        values.

    Raises
    ------
    ValueError
        If *format_type* is not in the set of allowed formats or if the
        data cannot be parsed according to that format.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    if fmt == "json":
        try:
            # json.loads expects a str; decode bytes safely using UTF-8
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        try:
            # CSV is read from a file-like object.  We use BytesIO to
            # avoid handling the raw bytes directly.
            with BytesIO(raw_data) as stream:
                text_stream = io.TextIOWrapper(stream, encoding="utf-8", newline="")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc

    # This point should never be reached because all allowed formats
    # are handled above.
    raise ValueError(f"Unhandled format: {format_type}")