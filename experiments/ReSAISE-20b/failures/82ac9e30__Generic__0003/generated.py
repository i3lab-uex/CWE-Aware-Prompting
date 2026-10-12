import json
import csv
import io
from typing import Any

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}


def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data as a byte stream.
    deserialization_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in the list of safe methods.
    """
    if deserialization_method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Convert bytes to string using UTF-8; errors='strict' will raise if invalid
    text = data_stream.decode("utf-8")

    if deserialization_method == "json":
        # json.loads safely parses JSON into Python objects
        return json.loads(text)

    if deserialization_method == "csv":
        # csv.DictReader reads CSV into a list of dictionaries
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached because of the SAFE_METHODS check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")