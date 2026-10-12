import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# Set of serialization formats that are considered safe and allowed.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified `format_name`.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data stream.
    format_name : str
        Name of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns the corresponding
        Python data structure (dict, list, etc.). For CSV it returns a list of
        dictionaries where each dictionary represents one row.

    Raises
    ------
    ValueError
        If `format_name` is not in the set of allowed formats or if decoding fails.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_name}'")

    try:
        if fmt == "json":
            # JSON decoding expects a string; decode bytes to UTF-8
            return json.loads(encoded_bytes.decode("utf-8"))
        elif fmt == "csv":
            # CSV decoding: read bytes as text, then parse rows into dicts
            with TextIOWrapper(BytesIO(encoded_bytes), encoding="utf-8") as text_stream:
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
    except Exception as exc:
        # Wrap any exception with a ValueError to keep the API consistent
        raise ValueError(f"Failed to decode data: {exc}") from exc