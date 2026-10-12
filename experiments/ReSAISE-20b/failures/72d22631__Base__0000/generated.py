import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Define a set of serialization methods that are considered safe
TRUSTED_METHODS = {"json", "csv"}


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Restore a Python object from serialized bytes using a specified method.

    Parameters
    ----------
    deserialized_bytes : bytes
        The serialized data stream.
    method_for_serialization : str
        The serialization format used, e.g., 'json', 'csv'.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    if not isinstance(deserialized_bytes, bytes):
        raise TypeError("deserialized_bytes must be of type 'bytes'")

    method = method_for_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or unsafe serialization method: '{method_for_serialization}'. "
            "Only 'json' and 'csv' are allowed."
        )

    # Decode bytes to string assuming UTF-8 encoding
    try:
        data_str = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Failed to decode bytes using UTF-8") from exc

    if method == "json":
        # json.loads is safe for standard JSON data
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Parse CSV into a list of dictionaries (one per row)
        try:
            reader = csv.DictReader(StringIO(data_str))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data") from exc

    # The following line should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {method}")