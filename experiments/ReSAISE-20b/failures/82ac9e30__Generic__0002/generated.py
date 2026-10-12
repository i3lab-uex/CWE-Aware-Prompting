import json
import csv
from io import StringIO

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into its corresponding Python object using only
    approved deserialization methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data in byte form.
    deserialization_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not recognized or disallowed.
    """
    if deserialization_method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Decode bytes to string using UTF-8; raise if decoding fails
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8.") from exc

    if deserialization_method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if deserialization_method == "csv":
        # Parse CSV into a list of dictionaries (header row as keys)
        try:
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data.") from exc