import json
import csv
import io
from typing import Any, Dict, List

# Define the set of safe and supported serialization formats.
ALLOWED_FORMATS = {
    "json",
    "csv",
}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize input data from a byte stream.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input data.
    format_name : str
        Name of the serialization format. Supported values are:
            - 'json': JSON encoded data.
            - 'csv' : CSV encoded data (converted to a list of dictionaries).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the list of allowed formats.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name!r}")

    # Decode bytes to string using UTF-8 (common encoding for text formats)
    try:
        text = encoded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # CSV is read as a list of dictionaries, one per row
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # The code path should never reach here because of the format check above.
    raise AssertionError("Unhandled serialization format")