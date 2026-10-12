import json
import csv
import io
from typing import Any

# List of serialization methods that are considered safe
_TRUSTED_METHODS = {
    "json",
    "csv",
}

def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Restore a Python object from a byte stream that was serialized using
    a trusted method.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    method_of_serialization : str
        Serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not in the list of trusted formats or if decoding/parsing fails.
    """
    method = method_of_serialization.lower()
    if method not in _TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization method: {method}")

    try:
        if method == "json":
            # Decode to text assuming UTF-8; raise on decoding errors
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if method == "csv":
            # CSV is parsed into a list of dictionaries
            text = byte_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]

    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
        raise ValueError(f"Failed to deserialize data using {method}") from exc