import json
import csv
import io
from typing import Any, List, Dict


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize a byte stream using only trusted serialization formats.

    Supported formats (case‑insensitive):
        - 'json': JSON data, returned as Python objects.
        - 'csv' : CSV data, returned as a list of dictionaries (header → value).

    Parameters
    ----------
    byte_data : bytes
        The raw data to deserialize.
    method_of_serialization : str
        Serialization format identifier.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unsupported or potentially dangerous.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    method = method_of_serialization.lower()
    # Ensure only safe formats are allowed
    if method == "json":
        try:
            decoded = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == "csv":
        try:
            decoded = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for CSV") from exc
        reader = csv.DictReader(io.StringIO(decoded))
        return [row for row in reader]

    else:
        # Reject all other methods (pickle, yaml, msgpack, etc.)
        raise ValueError(f"Unsupported or unsafe serialization method: {method_of_serialization}")