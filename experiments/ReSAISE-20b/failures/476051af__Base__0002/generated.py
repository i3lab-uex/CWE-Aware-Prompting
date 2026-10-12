import json
import configparser
from typing import Any

# A curated list of safe formats that are allowed for deserialization.
_SAFE_FORMATS = {
    "json": _deserialize_json,
    "ini": _deserialize_ini,
}

def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Safely deserialize binary data from trusted formats only.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        One of the supported format names ('json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered unsafe.
    """
    fmt = format_type.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    return _SAFE_FORMATS[fmt](bin_data)


def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data safely.
    """
    try:
        text = data.decode("utf-8")
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Failed to deserialize JSON data") from exc


def _deserialize_ini(data: bytes) -> dict:
    """
    Deserialize INI data into a nested dictionary.
    """
    try:
        text = data.decode("utf-8")
        parser = configparser.ConfigParser()
        parser.read_string(text)
    except (UnicodeDecodeError, configparser.Error) as exc:
        raise ValueError("Failed to deserialize INI data") from exc

    # Convert ConfigParser object into a plain dictionary
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result