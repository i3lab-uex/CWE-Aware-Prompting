import json
import configparser
from io import StringIO

def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary format.
    serialization_format : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or disallowed.
    """
    # Define a whitelist of safe formats
    _SAFE_FORMATS = {
        'json': _load_json,
        'ini' : _load_ini,
    }

    fmt = serialization_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or disallowed serialization format: {serialization_format}")

    return _SAFE_FORMATS[fmt](byte_data)


def _load_json(byte_data: bytes):
    """Deserialize JSON data."""
    try:
        text = byte_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data must be UTF-8 encoded") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _load_ini(byte_data: bytes):
    """Deserialize INI data into a nested dictionary."""
    try:
        text = byte_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("INI data must be UTF-8 encoded") from exc

    parser = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object; StringIO provides that
        parser.read_file(StringIO(text))
    except configparser.Error as exc:
        raise ValueError("Invalid INI data") from exc

    # Convert the parsed sections into a dictionary
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result