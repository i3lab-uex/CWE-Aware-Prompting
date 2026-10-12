import json
import csv
from io import BytesIO, TextIOWrapper

# List of serialization methods that are considered safe for deserialization
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into a Python object using the specified safe
    serialization format.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data as a byte string.
    format_method : str
        Identifier of the serialization method ('json', 'csv').

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_method is not in SAFE_METHODS or if deserialization fails.
    """
    method = format_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or unrecognized.")

    try:
        if method == "json":
            # json.loads expects a string, not bytes
            return json.loads(data_bytes.decode("utf-8"))

        if method == "csv":
            # Interpret bytes as text and parse with csv.DictReader
            text_stream = TextIOWrapper(BytesIO(data_bytes), encoding="utf-8")
            reader = csv.DictReader(text_stream)
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception from the deserialization libraries
        raise ValueError(f"Failed to deserialize data using method '{format_method}': {exc}") from exc