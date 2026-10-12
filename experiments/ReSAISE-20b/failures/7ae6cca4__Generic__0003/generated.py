import json
from configparser import ConfigParser
from typing import Any, Dict

class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or untrusted format is requested."""
    pass

def _parse_ini(data: str) -> Dict[str, Any]:
    """
    Convert an INI formatted string into a nested dictionary.
    Each section becomes a key whose value is another dict of the
    options inside that section. If no sections exist, a single
    section named 'DEFAULT' is used.
    """
    parser = ConfigParser()
    # read_string expects a string; we already decoded bytes
    parser.read_string(data)
    result: Dict[str, Any] = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    # Include default values (those not in any section)
    if parser.defaults():
        result.setdefault('DEFAULT', {}).update(parser.defaults())
    return result

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize `data_bytes` according to the trusted
    format specified by `format_string`.

    Supported formats:
        - 'json' : standard JSON
        - 'ini'  : INI configuration files

    Unsupported formats raise `UnsupportedFormatError`.

    Parameters
    ----------
    data_bytes : bytes
        The raw binary data received from an external source.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be bytes or bytearray")

    fmt = format_string.lower()
    if fmt == 'json':
        try:
            text = data_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == 'ini':
        try:
            text = data_bytes.decode('utf-8')
            return _parse_ini(text)
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid INI data") from exc

    # Any other format is considered untrusted
    raise UnsupportedFormatError(f"Unsupported or unsafe format: {format_string}")