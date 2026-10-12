import json
import csv
from io import StringIO, TextIOWrapper
from typing import Any


# Set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "csv"}


def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize a byte stream into a Python object using the specified format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized data as a byte string.
    format_name : str
        Name of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.  For JSON this will be a dict/list,
        for CSV it will be a list of rows (each row is a list of strings).

    Raises
    ------
    ValueError
        If `format_name` is not in the list of supported formats.
    """
    fmt = format_name.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_name}")

    # Decode the bytes to a text string (UTF‑8 is common for JSON/CSV)
    try:
        text = encoded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF‑8") from exc

    if fmt == "json":
        # json.loads is safe for JSON; it does not execute arbitrary code.
        return json.loads(text)

    if fmt == "csv":
        # Use csv.reader which only parses CSV syntax.
        f = StringIO(text)
        reader = csv.reader(f)
        return [row for row in reader]