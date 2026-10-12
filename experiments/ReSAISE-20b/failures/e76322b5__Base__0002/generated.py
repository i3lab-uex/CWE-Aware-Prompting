import json
import csv
import io
from typing import Any

# Whitelist of safe serialization formats
SAFE_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` using the specified `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input data.
    format_name : str
        Name of the serialization format. Supported values are
        "json" and "csv".

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the whitelist or if the data cannot be decoded.
    """
    fmt = format_name.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    # Common decoding step
    try:
        text = encoded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes are not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # Use csv.DictReader to parse CSV into list of dictionaries
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the whitelist check
    raise ValueError(f"Unhandled format: {format_name}")