import json
import configparser
from io import StringIO

# List of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {
    'json': _deserialize_json,
    'ini':  _deserialize_ini
}

def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized binary data.
    serialization_format : str
        The format used to serialize the data. Allowed values are
        'json' and 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the allowed list or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {serialization_format}")

    try:
        return ALLOWED_FORMATS[fmt](byte_data)
    except Exception as exc:
        # Wrap any exception in ValueError to avoid leaking internal details
        raise ValueError(f"Failed to deserialize data as {serialization_format}") from exc


def _deserialize_json(byte_data: bytes):
    """Deserialize JSON data."""
    # Decode bytes to string using UTF-8; errors='strict' ensures invalid encodings raise
    text = byte_data.decode('utf-8')
    return json.loads(text)


def _deserialize_ini(byte_data: bytes):
    """Deserialize INI data into a dictionary."""
    text = byte_data.decode('utf-8')
    parser = configparser.ConfigParser()
    # Use read_string to avoid file operations; it returns a ConfigParser instance
    parser.read_string(text)

    # Convert the ConfigParser structure to a plain dictionary
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result