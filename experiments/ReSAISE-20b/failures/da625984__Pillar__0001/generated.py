import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any, List, Dict

# Trusted serialization formats
_TRUSTED_METHODS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a Python object from the given byte stream using only
    trusted serialization methods.

    Parameters:
        byte_data (bytes): The serialized data stream.
        method_of_serialization (str): Serialization format identifier
            ('json', 'csv').

    Returns:
        Any: The deserialized Python object (dict, list, etc.).

    Raises:
        ValueError: If the method is unsupported or potentially unsafe.
    """
    if not isinstance(byte_data, bytes):
        raise ValueError("byte_data must be of type 'bytes'")

    method = method_of_serialization.lower()
    if method not in _TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization method: '{method_of_serialization}'")

    if method == "json":
        # Decode bytes to string and parse JSON
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF-8 encoded") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Treat CSV as a list of dictionaries (one per row)
        try:
            text_stream = TextIOWrapper(BytesIO(byte_data), encoding="utf-8", newline="")
        except Exception as exc:
            raise ValueError("CSV data must be UTF-8 encoded") from exc
        reader = csv.DictReader(text_stream)
        result: List[Dict[str, str]] = [row for row in reader]
        return result

    # The code path should never reach here because of the method check above
    raise ValueError(f"Unhandled serialization method: '{method_of_serialization}'")