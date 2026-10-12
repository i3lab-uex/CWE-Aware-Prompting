import json
import csv
import io
from typing import Any

# Define the set of allowed deserialization methods.
ALLOWED_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data.
    deserialization_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in the allowed list or if the data cannot be parsed.
    """
    method = deserialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    try:
        if method == "json":
            # Decode bytes to string and parse JSON.
            text = data_stream.decode("utf-8")
            return json.loads(text)

        if method == "csv":
            # Treat the byte stream as a CSV text.
            text = data_stream.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any parsing exception into a ValueError for consistency.
        raise ValueError(f"Failed to deserialize data using '{deserialization_method}': {exc}") from exc