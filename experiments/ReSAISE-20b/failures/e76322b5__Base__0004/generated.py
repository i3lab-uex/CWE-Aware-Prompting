import json
import csv
import io
from typing import Any

# Define the set of safe, supported serialization formats.
SAFE_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        The serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the whitelist of safe formats,
        or if the data cannot be decoded.
    """
    if not isinstance(encoded_bytes, bytes):
        raise ValueError("Input must be of type 'bytes'")

    fmt = format_name.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format '{format_name}'. "
                         f"Allowed formats: {', '.join(SAFE_FORMATS)}")

    # Decode the bytes to a string for text-based formats.
    try:
        decoded_text = encoded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Failed to decode bytes as UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(decoded_text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # Use StringIO to treat the string as a file for csv module.
        f = io.StringIO(decoded_text)
        reader = csv.DictReader(f)
        return list(reader)

    # In practice, this point is unreachable due to the whitelist check.
    raise ValueError(f"Unhandled format '{format_name}'")