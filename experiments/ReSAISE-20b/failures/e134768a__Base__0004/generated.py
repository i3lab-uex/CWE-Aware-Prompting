import json
import configparser
from typing import Any


# List of safe formats allowed for deserialization.
ALLOWED_FORMATS = {
    "json": _deserialize_json,
    "ini": _deserialize_ini,
}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data that comes from an untrusted source.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        One of the supported formats.  Currently only ``json`` and ``ini``
        are considered safe.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or considered unsafe.
    """
    fmt = struct_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    return ALLOWED_FORMATS[fmt](byte_data)


def _deserialize_json(byte_data: bytes) -> Any:
    """Deserialize JSON data from a byte string."""
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF‑8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON data") from exc


def _deserialize_ini(byte_data: bytes) -> configparser.ConfigParser:
    """Deserialize INI data from a byte string."""
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("INI data is not valid UTF‑8") from exc

    parser = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object; we use read_string.
        parser.read_string(text)
    except configparser.Error as exc:
        raise ValueError("Malformed INI data") from exc

    return parser