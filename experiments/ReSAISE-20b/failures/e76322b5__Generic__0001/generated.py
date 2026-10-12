import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize input data from a given serialization format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        The name of the serialization format ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it can be any valid
        JSON structure; for CSV a list of dictionaries is returned.

    Raises
    ------
    ValueError
        If the format_name is not in ALLOWED_FORMATS or if decoding fails.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    try:
        text = encoded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded using UTF-8") from exc

    if fmt == "json":
        # json.loads is safe for standard JSON data.
        return json.loads(text)

    if fmt == "csv":
        # Parse CSV into a list of dictionaries (each row as dict).
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # The above check should prevent reaching here, but keep it as a safety net.
    raise ValueError(f"Unhandled format: {format_name}")