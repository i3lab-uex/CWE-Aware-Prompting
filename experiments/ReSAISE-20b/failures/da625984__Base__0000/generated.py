import json
import csv
import io
from typing import Any, List, Dict


def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize a byte stream using only trusted formats.

    Supported formats:
        - 'json' : JSON encoded data
        - 'csv'  : CSV encoded data (returns a list of dicts)

    Args:
        byte_data: The serialized data as bytes.
        method_of_serialization: Name of the serialization format.

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the serialization method is unsupported or potentially unsafe.
    """
    # Ensure we have a bytes object
    if not isinstance(byte_data, (bytes, bytearray)):
        raise ValueError("Input data must be bytes or bytearray")

    method = method_of_serialization.lower()

    if method == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if method == "csv":
        try:
            text = byte_data.decode("utf-8")
            f = io.StringIO(text)
            reader = csv.DictReader(f)
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV data") from exc

    # Any other method is considered unsafe or unsupported
    raise ValueError(f"Unsupported serialization format: {method_of_serialization}")