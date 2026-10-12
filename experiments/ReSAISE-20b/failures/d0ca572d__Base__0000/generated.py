import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Define a whitelist of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using a whitelisted method.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not in SAFE_METHODS or if decoding fails.
    """
    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed.")

    try:
        # Decode bytes to string assuming UTF-8 encoding
        text = data_bytes_stream.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode data bytes: {exc}") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if method == "csv":
        try:
            # Use csv.DictReader to return a list of dictionaries
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"CSV deserialization error: {exc}") from exc

    # The code should never reach here because of the whitelist check
    raise ValueError(f"Unsupported serialization method: {method_of_serialization}")