import json
import csv
from io import BytesIO, StringIO

# List of allowed deserialization methods
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    data_stream : bytes
        The serialized data as a byte stream.
    deserialization_method : str
        Identifier of the serialization method ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not recognized or not allowed.
    """
    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    if method == "json":
        # Decode bytes to str and load JSON
        text = data_stream.decode("utf-8")
        return json.loads(text)

    if method == "csv":
        # CSV is read as text; use StringIO
        text = data_stream.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")