import json
from typing import Any


def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize data from raw bytes into a Python object.

    Parameters
    ----------
    data_bytes : bytes
        Serialized representation of the object.
    format_name : str
        The serialization format used. Supported formats are:
        - 'json'  (safe and recommended)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided format is not supported or considered unsafe.
    """
    # Normalize format name to lowercase for comparison
    fmt = format_name.strip().lower()

    if fmt == "json":
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data bytes are not valid UTF-8 for JSON.") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    # If you wish to support additional safe formats, add them here.
    # For example: 'msgpack', 'toml', etc. (ensure they are safe for untrusted input)

    # If format is not supported, raise an error
    raise ValueError(f"Unsupported or unsafe serialization format: {format_name!r}")