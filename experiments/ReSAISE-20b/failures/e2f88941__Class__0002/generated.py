import json
import csv
from io import StringIO, BytesIO
from typing import Any

# List of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized methods.

    Parameters:
        data_bytes (bytes): The serialized data.
        format_method (str): Identifier of the serialization method
            ('json' or 'csv').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format_method is not supported or disallowed.
    """
    method = format_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or disallowed serialization method: {format_method}")

    # Handle JSON deserialization
    if method == "json":
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc
        return json.loads(text)

    # Handle CSV deserialization
    if method == "csv":
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for CSV deserialization") from exc
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # The code should never reach here due to the ALLOWED_METHODS check
    raise ValueError(f"Unhandled serialization method: {format_method}")