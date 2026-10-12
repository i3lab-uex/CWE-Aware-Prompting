import json
import configparser
from typing import Any, Union

def safely_deserialize_data(
    serialized_bytes: bytes,
    method_format: str
) -> Any:
    """
    Deserialize binary data safely using only approved formats.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary representation of the data.
    method_format : str
        Serialization format identifier (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or not in the whitelist.
    """
    # Define a whitelist of safe formats
    _SAFE_FORMATS = {
        "json": _deserialize_json,
        "ini": _deserialize_ini
    }

    fmt = method_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: '{method_format}'")

    return _SAFE_FORMATS[fmt](serialized_bytes)


def _deserialize_json(data: bytes) -> Union[list, dict]:
    """
    Deserialize JSON data. The input must be valid UTF-8 encoded.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF-8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _deserialize_ini(data: bytes) -> configparser.ConfigParser:
    """
    Deserialize INI data. Returns a ConfigParser instance.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("INI data is not valid UTF-8") from exc

    parser = configparser.ConfigParser()
    try:
        # read_string expects a string; use read_file if reading from file-like
        parser.read_string(text)
    except configparser.Error as exc:
        raise ValueError("Invalid INI data") from exc

    return parser