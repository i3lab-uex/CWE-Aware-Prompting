import json
import csv
from io import StringIO, BytesIO

# Define the set of safe serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str):
    """
    Deserialize `encoded_bytes` according to the specified `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        Name of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if not isinstance(encoded_bytes, (bytes, bytearray)):
        raise TypeError("encoded_bytes must be a bytes-like object")

    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_name!r}")

    # Decode bytes to text using UTF-8 (common default)
    text = encoded_bytes.decode("utf-8")

    if fmt == "json":
        return json.loads(text)

    # CSV handling: returns a list of dicts (header as keys)
    if fmt == "csv":
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # Should never reach here due to the earlier check
    raise ValueError(f"Unhandled format: {format_name!r}")