import json
import csv
from io import BytesIO, TextIOWrapper

# List of serialization methods that are considered safe for deserialization
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into a Python object using only safe methods.

    Parameters
    ----------
    data_bytes : bytes
        The serialized byte stream.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_METHODS or is unrecognized.
    """
    method = format_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or unknown.")

    if method == "json":
        # json.loads expects a str; decode bytes safely using UTF-8
        return json.loads(data_bytes.decode("utf-8"))

    if method == "csv":
        # CSV data is decoded to text and parsed into a list of dictionaries
        with BytesIO(data_bytes) as byte_stream:
            # Wrap the binary stream in a text wrapper that decodes using UTF-8
            with TextIOWrapper(byte_stream, encoding="utf-8") as text_stream:
                reader = csv.DictReader(text_stream)
                return [row for row in reader]

    # This point should never be reached because of the earlier check
    raise ValueError(f"Unhandled deserialization method: {format_method}")