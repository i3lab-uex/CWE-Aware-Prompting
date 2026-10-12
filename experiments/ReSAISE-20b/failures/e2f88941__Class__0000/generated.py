import json
import csv
from io import BytesIO, StringIO

# List of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into a Python object using only safe
    serialization methods.

    Parameters:
        data_bytes (bytes): The serialized byte stream.
        format_method (str): Identifier of the serialization method
                             ('json', 'csv').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format_method is not recognized or disallowed.
    """
    if format_method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or disallowed serialization method: {format_method}")

    if format_method == "json":
        # json.loads expects a string, so decode using UTF-8
        text = data_bytes.decode("utf-8")
        return json.loads(text)

    if format_method == "csv":
        # Decode bytes to text, then use csv.DictReader
        text = data_bytes.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {format_method}")