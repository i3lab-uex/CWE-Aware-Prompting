import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Define a set of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using a
    safe, explicitly permitted serialization method.

    Parameters:
        data_bytes_stream (bytes): The serialized data as bytes.
        method_of_serialization (str): Identifier of the serialization method
            used, e.g. 'json', 'csv'.

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the method is not recognized or disallowed.
    """
    if method_of_serialization not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed")

    if method_of_serialization == "json":
        # JSON requires UTF‑8 encoding
        text = data_bytes_stream.decode("utf-8")
        return json.loads(text)

    if method_of_serialization == "csv":
        # Interpret bytes as UTF‑8 text and parse with csv.reader
        text_stream = StringIO(data_bytes_stream.decode("utf-8"))
        reader = csv.reader(text_stream)
        # Convert to a list of rows; each row is a list of strings
        return [row for row in reader]

    # The code path should never reach here because of the guard above
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")