import json
import configparser
from io import BytesIO


def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Safely deserialize binary data from a restricted set of formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data to deserialize.
    serialization_format : str
        The format used for serialization. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the provided format is not in the allowed list or if deserialization fails.
    """
    # Define a whitelist of safe formats
    _ALLOWED_FORMATS = {
        'json': _deserialize_json,
        'ini': _deserialize_ini,
    }

    fmt = serialization_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {serialization_format!r}")

    # Call the corresponding deserializer
    return _ALLOWED_FORMATS[fmt](byte_data)


def _deserialize_json(byte_data: bytes):
    try:
        return json.loads(byte_data.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Failed to deserialize JSON data") from exc


def _deserialize_ini(byte_data: bytes):
    """
    Deserialize INI formatted data into a dictionary of dictionaries.
    """
    parser = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object
        parser.read_file(BytesIO(byte_data))
    except configparser.Error as exc:
        raise ValueError("Failed to deserialize INI data") from exc

    # Convert the parser object into a plain dictionary
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result