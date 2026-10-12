import json
import csv
from io import BytesIO
from typing import Any

# List of serialization methods that are considered safe.
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not recognized or disallowed.
    """
    if format_method.lower() not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed.")

    if format_method.lower() == "json":
        # Decode bytes to string and parse JSON.
        return json.loads(data_bytes.decode("utf-8"))

    if format_method.lower() == "csv":
        # Use csv.DictReader to parse CSV data into a list of dictionaries.
        with BytesIO(data_bytes) as f:
            reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8"))
            return [row for row in reader]

    # The SAFE_METHODS set guarantees that we never reach here,
    # but this is a defensive fallback.
    raise ValueError(f"Unhandled serialization method: {format_method}")