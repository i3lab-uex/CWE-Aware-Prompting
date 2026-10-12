import json
import configparser
from typing import Any

class UnsafeFormatError(ValueError):
    """Raised when the requested format is not allowed for deserialization."""
    pass

def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Safely deserialize binary data using only a whitelisted set of formats.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary data received from an external source.
    method_format : str
        The format used to serialize the data. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsafeFormatError
        If the requested format is not in the allowed list.
    ValueError
        If deserialization fails due to malformed data or unsupported content.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {
        'json': _deserialize_json,
        'ini' : _deserialize_ini
    }

    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise UnsafeFormatError(f"Deserialization format '{method_format}' is not allowed.")

    # Call the corresponding deserializer
    return SAFE_FORMATS[fmt](serialized_bytes)


def _deserialize_json(data: bytes) -> Any:
    """Deserialize JSON data from bytes."""
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF-8.") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON data.") from exc


def _deserialize_ini(data: bytes) -> dict:
    """Deserialize INI data from bytes into a nested dictionary."""
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("INI data is not valid UTF-8.") from exc

    parser = configparser.ConfigParser()
    try:
        parser.read_string(text)
    except configparser.Error as exc:
        raise ValueError("Malformed INI data.") from exc

    # Convert ConfigParser object to a plain dictionary
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result