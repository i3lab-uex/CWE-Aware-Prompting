import json
import csv
import io
from typing import Any

# Define the list of safe serialization methods
SAFE_METHODS = {"json", "csv"}


def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only authorized methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is disallowed or not recognized.
    """
    if method_of_serialization not in SAFE_METHODS:
        raise ValueError(
            f"Deserialization method '{method_of_serialization}' is not allowed."
        )

    # Decode bytes to a string; assume UTF-8 encoding
    try:
        data_str = data_bytes_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8.") from exc

    if method_of_serialization == "json":
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data.") from exc

    if method_of_serialization == "csv":
        # Use csv.DictReader to produce a list of dictionaries
        try:
            f = io.StringIO(data_str)
            reader = csv.DictReader(f)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data.") from exc

    # The following line is unreachable due to the SAFE_METHODS check,
    # but kept for completeness.
    raise ValueError(f"Unsupported serialization method: {method_of_serialization}")