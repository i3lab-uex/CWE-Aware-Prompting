import json
import csv
from io import BytesIO
from typing import Any

# Allowed serialization formats
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize the given byte stream according to the specified format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data.
    format_name : str
        Name of the serialization format. Supported values are:
        - 'json'
        - 'csv'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or potentially insecure format is requested.
    """
    if not isinstance(encoded_bytes, (bytes, bytearray)):
        raise ValueError("encoded_bytes must be a bytes-like object")

    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_name}")

    if fmt == "json":
        # json.loads expects a str, so decode using UTF-8
        try:
            text = encoded_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 encoding for JSON data") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # csv module works with text streams; wrap bytes in BytesIO and decode line by line
        try:
            stream = BytesIO(encoded_bytes)
            # Use UTF-8 decoding; errors='replace' ensures graceful handling of malformed bytes
            reader = csv.DictReader(
                (line.decode("utf-8", errors="replace") for line in stream),
            )
            return list(reader)
        except Exception as exc:
            raise ValueError("Failed to parse CSV data") from exc

    # This point should never be reached because of the earlier check
    raise ValueError(f"Unhandled format: {format_name}")