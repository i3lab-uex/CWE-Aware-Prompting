import json
import csv
import io
from typing import Any


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize a byte stream using only trusted formats.

    Supported formats (case‑insensitive):
        - 'json':   JSON text encoded in UTF‑8
        - 'csv' :   CSV data encoded in UTF‑8; returns a list of dictionaries

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    method_of_serialization : str
        Name of the serialization format.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Normalise the format name
    fmt = method_of_serialization.strip().lower()

    if fmt == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if fmt == "csv":
        try:
            text = byte_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV data") from exc

    # Disallow potentially dangerous formats such as pickle, marshal, etc.
    raise ValueError(f"Unsupported or unsafe serialization method: {method_of_serialization}")