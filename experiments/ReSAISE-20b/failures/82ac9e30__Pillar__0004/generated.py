import json
import csv
import io

# Safe, predefined list of serialization methods.
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into a Python object using only safe methods.

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
        If the method is not recognized or disallowed.
    """
    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Decode bytes to string; assume UTF-8 encoding.
    try:
        text = data_stream.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode data stream: {exc}") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == "csv":
        # Use StringIO to create a file-like object for csv reader.
        with io.StringIO(text) as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    # Should never reach here due to earlier check, but keep for completeness.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")