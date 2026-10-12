import json
import csv
import io
from typing import Any

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` using the specified serialization `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data stream.
    format_name : str
        Name of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the list of allowed formats or if deserialization fails.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_name}")

    try:
        if fmt == "json":
            # JSON is safe by default; use json.loads on decoded string.
            return json.loads(encoded_bytes.decode("utf-8"))

        if fmt == "csv":
            # CSV is read into a list of dictionaries.
            decoded_str = encoded_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded_str))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any deserialization exception into a ValueError for consistency.
        raise ValueError(f"Failed to decode data as {format_name}: {exc}") from exc