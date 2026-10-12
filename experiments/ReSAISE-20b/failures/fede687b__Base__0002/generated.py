import json
import csv
from io import StringIO

# Set of serialization formats that are considered safe for untrusted input.
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object using the specified
    serialization format.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        One of the supported serialization formats ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python data structure.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type!r}")

    try:
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Input data is not valid UTF‑8: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "csv":
        # Read CSV into a list of dictionaries (first row as header)
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled format: {format_type!r}")