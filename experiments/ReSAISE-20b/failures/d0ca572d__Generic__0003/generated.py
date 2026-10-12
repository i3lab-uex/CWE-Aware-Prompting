import json
import csv
from io import BytesIO
from typing import Any

# List of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization format used ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not in SAFE_METHODS or if deserialization fails.
    """
    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Disallowed or unrecognized serialization method: {method_of_serialization}")

    try:
        if method == "json":
            # json.loads expects a string, so decode bytes using UTF-8
            return json.loads(data_bytes_stream.decode("utf-8"))
        elif method == "csv":
            # Use csv.DictReader to parse CSV into a list of dictionaries
            stream = BytesIO(data_bytes_stream)
            # Assume UTF-8 encoding; adjust if necessary
            reader = csv.DictReader(
                (line.decode("utf-8") for line in stream),
                delimiter=",",
                quotechar='"',
            )
            return [row for row in reader]
    except Exception as exc:
        raise ValueError(f"Failed to deserialize using {method_of_serialization}: {exc}") from exc