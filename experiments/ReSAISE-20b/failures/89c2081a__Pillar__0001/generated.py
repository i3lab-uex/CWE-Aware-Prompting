import json
from configparser import ConfigParser, NoSectionError, NoOptionError
from io import StringIO

class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or unsafe format is requested."""

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary payloads using only safe formats.

    Parameters
    ----------
    payload_bytes : bytes
        The serialized data in binary form.
    schema_type : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    object
        The Python representation of the data.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not in the curated list.
    ValueError
        If deserialization fails (e.g., malformed data).
    """
    # Map allowed formats to their handlers
    _SAFE_FORMATS = {
        'json': _deserialize_json,
        'ini' : _deserialize_ini
    }

    fmt = schema_type.lower()
    if fmt not in _SAFE_FORMATS:
        raise UnsupportedFormatError(
            f"Unsupported or unsafe format '{schema_type}'. "
            "Allowed formats: 'json', 'ini'."
        )

    return _SAFE_FORMATS[fmt](payload_bytes)

def _deserialize_json(payload: bytes):
    try:
        text = payload.decode('utf-8')
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

def _deserialize_ini(payload: bytes):
    try:
        text = payload.decode('utf-8')
        parser = ConfigParser()
        parser.read_file(StringIO(text))
    except Exception as exc:
        raise ValueError(f"Failed to deserialize INI: {exc}") from exc

    result = {}
    for section in parser.sections():
        items = dict(parser.items(section))
        result[section] = items
    return result