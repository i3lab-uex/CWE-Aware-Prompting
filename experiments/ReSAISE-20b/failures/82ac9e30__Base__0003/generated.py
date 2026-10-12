import json
import csv
import io
from typing import Any

# Define the list of allowed deserialization methods.
ALLOWED_METHODS = {
    'json',
    'csv',
}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    data_stream : bytes
        The serialized data.
    deserialization_method : str
        The name of the serialization format ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not in ALLOWED_METHODS or if deserialization fails.
    """
    method = deserialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    try:
        if method == 'json':
            # Decode bytes to string and parse JSON
            text = data_stream.decode('utf-8')
            return json.loads(text)

        if method == 'csv':
            # Decode bytes to string and parse CSV into a list of dictionaries
            text = data_stream.decode('utf-8')
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception to avoid leaking internal details
        raise ValueError(f"Failed to deserialize data using '{deserialization_method}': {exc}") from None