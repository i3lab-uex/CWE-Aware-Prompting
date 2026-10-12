import json
import csv
from io import BytesIO
from typing import Any

# Define a set of serialization formats that are considered safe.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data stream.
    format_name : str
        The name of the serialization format. Must be one of the values in
        `ALLOWED_FORMATS`. Case-insensitive.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the allowed set.
    """
    if not isinstance(encoded_bytes, (bytes, bytearray)):
        raise TypeError("encoded_bytes must be a bytes-like object")

    fmt = format_name.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_name}'")

    # Handle JSON
    if fmt == "json":
        try:
            return json.loads(encoded_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    # Handle CSV
    if fmt == "csv":
        try:
            stream = BytesIO(encoded_bytes)
            reader = csv.DictReader(
                (line.decode("utf-8") for line in stream),
                delimiter=",",
            )
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV data") from exc

    # This point should never be reached because of the check above
    raise ValueError(f"Unhandled format: {format_name}")