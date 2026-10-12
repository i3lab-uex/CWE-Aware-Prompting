import json
import configparser
from typing import Any

# Define the list of trusted formats
TRUSTED_FORMATS = {
    'json': _decode_json,
    'ini': _decode_ini,
}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format string.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data.
    format_string : str
        Identifier of the serialization format (e.g. 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or untrusted.
    """
    fmt = format_string.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    decode_func = TRUSTED_FORMATS[fmt]
    return decode_func(data_bytes)


def _decode_json(data_bytes: bytes) -> Any:
    """
    Decode JSON data. Enforces UTF-8 decoding and uses json.loads.
    """
    try:
        text = data_bytes.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data must be UTF-8 encoded") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _decode_ini(data_bytes: bytes) -> dict:
    """
    Decode INI data into a nested dictionary. Uses configparser which is safe
    for plain text configurations.
    """
    try:
        text = data_bytes.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("INI data must be UTF-8 encoded") from exc

    parser = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object
        parser.read_string(text)
    except configparser.Error as exc:
        raise ValueError("Invalid INI data") from exc

    # Convert to a plain dict of dicts
    result = {section: dict(parser.items(section)) for section in parser.sections()}
    return result