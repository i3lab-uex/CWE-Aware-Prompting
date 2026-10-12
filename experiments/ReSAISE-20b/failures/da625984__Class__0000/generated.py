import json
import csv
import io
from typing import Any

# List of trusted serialization formats
TRUSTED_METHODS = {"json", "csv"}

def deserialize_obj(byte_data: bytes, method_of_serialization: str) -> Any:
    """
    Restore a Python object from serialized byte data.

    Parameters
    ----------
    byte_data : bytes
        The raw byte stream containing the serialized data.
    method_of_serialization : str
        The serialization format used. Supported formats are 'json' and 'csv'.

    Returns
    -------
    Any
        The deserialized Python object. For JSON, this may be a dict, list,
        str, int, float, bool or None. For CSV, this is a list of dicts,
        each representing one row with column names as keys.

    Raises
    ------
    ValueError
        If the requested serialization method is not trusted or unsupported.
    """
    method = method_of_serialization.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or potentially unsafe serialization method: {method_of_serialization}")

    # Convert bytes to a text stream
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # csv.reader expects a file-like object; use StringIO
        f = io.StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # This point should never be reached due to the TRUSTED_METHODS check
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")