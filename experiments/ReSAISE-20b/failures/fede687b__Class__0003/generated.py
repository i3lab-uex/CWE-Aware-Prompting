import json
import csv
from io import BytesIO, TextIOWrapper

# Allowed serialization formats
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str):
    """
    Deserialize `raw_data` according to the specified `format_type`.

    Parameters
    ----------
    raw_data : bytes
        Serialized data to be deserialized.
    format_type : str
        Serialization format. Supported values are 'json' and 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of allowed formats.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    # Ensure the bytes are decoded using UTF-8 (most common for text formats)
    try:
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8") from exc

    if fmt == "json":
        # json.loads is safe for deserialization of standard JSON data
        return json.loads(text)

    if fmt == "csv":
        # Use csv.DictReader to parse CSV into a list of dictionaries
        # Wrap the string in a BytesIO for compatibility with TextIOWrapper
        buffer = BytesIO(raw_data)
        reader = csv.DictReader(TextIOWrapper(buffer, encoding="utf-8"))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_type}")