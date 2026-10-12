import json
import csv
from io import BytesIO

# Define the list of safe serialization methods.
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into a Python object using only authorized
    serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization method ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not recognized or disallowed.
    """
    if method_of_serialization not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed")

    if method_of_serialization == "json":
        # Decode bytes to str, then load JSON.
        try:
            text = data_bytes_stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode JSON bytes") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method_of_serialization == "csv":
        # Parse CSV into a list of dictionaries.
        try:
            text = data_bytes_stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV bytes") from exc
        try:
            reader = csv.DictReader(text.splitlines())
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data") from exc