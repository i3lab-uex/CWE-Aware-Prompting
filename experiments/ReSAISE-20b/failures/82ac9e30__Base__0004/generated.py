import json
import csv
from io import StringIO
from typing import Any

# List of allowed deserialization methods
ALLOWED_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only authorized methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data as a byte stream.
    deserialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not supported or disallowed.
    """
    if deserialization_method.lower() not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Decode the byte stream to a string using UTF-8 (common for text formats)
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8.") from exc

    if deserialization_method.lower() == "json":
        # Use json.loads which is safe for untrusted data
        return json.loads(text)

    if deserialization_method.lower() == "csv":
        # Parse CSV into a list of dictionaries (one per row)
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # The code should never reach here due to the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")