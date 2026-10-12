import json
import csv
from io import StringIO, BytesIO
from typing import Any

# List of allowed serialization methods
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using the specified format.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        Identifier of the serialization method (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_method is not in SAFE_METHODS or if deserialization fails.
    """
    method = format_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or recognized.")

    try:
        if method == "json":
            # json expects a string, so decode using utf-8
            return json.loads(data_bytes.decode("utf-8"))

        if method == "csv":
            # Convert bytes to text and read with csv.DictReader
            text = data_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into ValueError to keep the API consistent
        raise ValueError(f"Failed to deserialize data using '{format_method}': {exc}") from exc