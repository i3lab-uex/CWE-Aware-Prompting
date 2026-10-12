import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Trusted serialization formats
_TRUSTED_METHODS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Safely deserialize `byte_data` according to the specified serialization method.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    method_of_serialization : str
        Serialization format to use ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a Python dict/list/primitive.
        For CSV, a list of dictionaries (one per row) with string values.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    method = method_of_serialization.lower()
    if method not in _TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or unsafe serialization method: {method_of_serialization}"
        )

    if method == "json":
        # Decode bytes to str and parse JSON
        text = byte_data.decode("utf-8")
        return json.loads(text)

    if method == "csv":
        # Decode bytes to str and parse CSV
        text = byte_data.decode("utf-8")
        f = StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # Should never reach here because of the whitelist
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")