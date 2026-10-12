import json
import csv
from io import StringIO

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into its corresponding Python object using only
    whitelisted serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized byte stream.
    method_of_serialization : str
        Identifier of the serialization format ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is disallowed or not recognized.
    """
    # Whitelisted safe methods
    SAFE_METHODS = {"json", "csv"}

    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Disallowed or unrecognized serialization method: {method_of_serialization}")

    # Decode bytes to string
    try:
        text = data_bytes_stream.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data bytes could not be decoded using UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Parse CSV into a list of dictionaries (first row as header)
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]