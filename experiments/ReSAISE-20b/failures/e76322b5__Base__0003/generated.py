import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Whitelisted serialization formats
ALLOWED_FORMATS = {"json", "csv"}


def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize input data from the specified format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        The name of the serialization format. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object. For `json` this is whatever the JSON data represents.
        For `csv` it returns a list of dictionaries (one per row).

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    try:
        text = encoded_bytes.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Input bytes could not be decoded as UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        try:
            f = StringIO(text)
            reader = csv.DictReader(f)
            return [row for row in reader]
        except Exception as exc:  # pragma: no cover
            raise ValueError("Invalid CSV data") from exc

    # This point should never be reached due to the whitelist check
    raise ValueError(f"Unhandled format: {format_name}")