import json
import configparser
from io import BytesIO

# Safe deserialization formats
_SAFE_FORMATS = {
    'json': _deserialize_json,
    'ini':  _deserialize_ini
}

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Deserialize binary data using a safe and pre‑approved format.

    Parameters
    ----------
    bin_data : bytes
        Serialized data.
    format_type : str
        Format identifier ('json' or 'ini').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    fmt = format_type.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    return _SAFE_FORMATS[fmt](bin_data)

def _deserialize_json(data: bytes):
    """Deserialize JSON data."""
    try:
        text = data.decode('utf-8')
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid JSON data: {exc}") from exc

def _deserialize_ini(data: bytes):
    """Deserialize INI data into a dictionary."""
    parser = configparser.ConfigParser()
    try:
        with BytesIO(data) as stream:
            parser.read_file(stream)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid INI data: {exc}") from exc

    # Convert to a plain dict of dicts
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result