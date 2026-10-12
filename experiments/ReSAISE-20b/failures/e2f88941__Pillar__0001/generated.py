import json
import csv
from io import BytesIO, TextIOWrapper

# List of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_method is not in ALLOWED_METHODS or is unrecognized.
    """
    if format_method not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or recognized.")

    if format_method == "json":
        # json.loads expects a str, so decode using UTF-8
        return json.loads(data_bytes.decode("utf-8"))

    if format_method == "csv":
        # Treat the bytes as a CSV file.  Use TextIOWrapper to decode.
        with BytesIO(data_bytes) as byte_stream:
            text_stream = TextIOWrapper(byte_stream, encoding="utf-8", newline="")
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    # If we reach here, the method is unknown (should not happen due to check above)
    raise ValueError(f"Unsupported serialization format: {format_method}")