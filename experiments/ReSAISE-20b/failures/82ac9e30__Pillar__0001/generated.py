import json
import csv
import io

# List of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    data_stream : bytes
        The serialized data in binary form.
    deserialization_method : str
        One of the supported methods ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not supported or data_stream is invalid.
    """
    if not isinstance(data_stream, bytes):
        raise ValueError("data_stream must be of type 'bytes'")

    method = deserialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed")

    # Decode bytes to text using UTF-8
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("data_stream is not valid UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Use StringIO to treat the text as a file-like object
        f = io.StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # The code should never reach here because of the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")