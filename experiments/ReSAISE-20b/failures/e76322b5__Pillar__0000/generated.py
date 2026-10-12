import json
import csv
from io import StringIO, BytesIO
from typing import Any

# A set of serialization formats that are considered safe for this context.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The raw serialized data.
    format_name : str
        Name of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the set of allowed formats.
    """
    format_name = format_name.lower()
    if format_name not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization method: {format_name}")

    if format_name == "json":
        # JSON decoding is safe when using json.loads on a string.
        text = encoded_bytes.decode("utf-8")
        return json.loads(text)

    if format_name == "csv":
        # CSV decoding: read the bytes as text and parse into a list of dictionaries.
        with StringIO(encoded_bytes.decode("utf-8")) as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    # This point should never be reached because of the guard above.
    raise ValueError(f"Unhandled format: {format_name}")