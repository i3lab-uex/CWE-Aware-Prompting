import json
import csv
import io
from typing import Any, List, Dict


# Accepted serialization formats (safe by design)
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize the given byte stream according to the specified method type.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        One of the supported serialization formats: 'json' or 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.
        - For JSON: the corresponding Python data structure (dict, list, etc.).
        - For CSV: a list of dictionaries representing rows.

    Raises
    ------
    ValueError
        If the method_type is not supported or if deserialization fails.
    """
    # Normalise method type
    fmt = method_type.lower()
    if fmt not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported serialization method: {method_type!r}")

    # Decode bytes to text (UTF-8 is the common default)
    try:
        text = stream_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data") from exc

    if fmt == "csv":
        # Use csv.DictReader to parse CSV into list of dicts
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached because of the ALLOWED_METHODS check
    raise ValueError(f"Unhandled serialization method: {method_type!r}")