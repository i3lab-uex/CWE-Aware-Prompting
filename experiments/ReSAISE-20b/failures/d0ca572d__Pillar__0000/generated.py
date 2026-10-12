import json
import csv
from io import BytesIO, TextIOWrapper

# List of allowed serialization methods
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into its corresponding Python object using
    only authorized serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data.
    method_of_serialization : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is disallowed or not recognized.
    """
    method = method_of_serialization.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed.")

    if method == "json":
        # Decode bytes to string using UTF-8 (common default)
        try:
            text = data_bytes_stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data stream is not valid UTF-8 for JSON deserialization.") from exc
        return json.loads(text)

    if method == "csv":
        # Wrap bytes in a TextIOWrapper to use csv.reader
        with BytesIO(data_bytes_stream) as byte_buffer:
            text_wrapper = TextIOWrapper(byte_buffer, encoding="utf-8")
            reader = csv.reader(text_wrapper)
            return [row for row in reader]

    # The code should never reach here because of the SAFE_METHODS check,
    # but a fallback for future safety.
    raise ValueError(f"Unsupported serialization method: {method_of_serialization}")