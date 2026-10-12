import json
import csv
from io import StringIO, BytesIO
from typing import Any


def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    approved serialization methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data as a byte stream.
    deserialization_method : str
        Identifier of the serialization method used
        ('json' or 'csv').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the method is not recognized or not permitted.
    """
    # Define a whitelist of safe deserialization methods
    SAFE_METHODS = {
        'json': _deserialize_json,
        'csv': _deserialize_csv
    }

    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Delegate to the appropriate function
    return SAFE_METHODS[method](data_stream)


def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data from a byte stream.
    """
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF-8.") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data.") from exc


def _deserialize_csv(data: bytes) -> list[list[str]]:
    """
    Deserialize CSV data from a byte stream.
    Returns a list of rows, each row being a list of strings.
    """
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("CSV data is not valid UTF-8.") from exc

    # Use StringIO to allow csv.reader to work with string data
    reader = csv.reader(StringIO(text))
    return [row for row in reader]