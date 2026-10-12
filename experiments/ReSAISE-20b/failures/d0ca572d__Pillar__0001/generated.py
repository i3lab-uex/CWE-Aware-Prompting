import json
import csv
import pickle
from io import BytesIO, TextIOWrapper
from typing import Any

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv", "pickle"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a data stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized byte stream.
    method_of_serialization : str
        Identifier of the serialization format used.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not recognized or disallowed.
    """
    if method_of_serialization.lower() not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed.")

    # Use a BytesIO wrapper to provide a file-like interface
    byte_stream = BytesIO(data_bytes_stream)

    if method_of_serialization.lower() == "json":
        # JSON is text based; decode to str
        with TextIOWrapper(byte_stream, encoding="utf-8") as text_stream:
            return json.load(text_stream)

    if method_of_serialization.lower() == "csv":
        # CSV is text based; decode to str
        with TextIOWrapper(byte_stream, encoding="utf-8") as text_stream:
            reader = csv.DictReader(text_stream)
            return list(reader)

    if method_of_serialization.lower() == "pickle":
        # Pickle is binary; use pickle.loads directly
        return pickle.loads(data_bytes_stream)

    # This point should never be reached due to earlier check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")