import json
import configparser
from typing import Any, Dict


# Allowed formats for deserialization – only those that are considered safe
ALLOWED_FORMATS = {
    "json": _decode_json,
    "ini":  _decode_ini,
}


def _decode_json(data: bytes) -> Any:
    """
    Safely decode JSON data.
    The json module only creates basic Python objects (dict, list, str,
    int, float, bool, None), which cannot execute code.
    """
    try:
        return json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Invalid JSON data") from exc


def _decode_ini(data: bytes) -> Dict[str, Any]:
    """
    Safely decode INI data using configparser.
    The result is a nested dictionary where values are strings.
    """
    parser = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object; BytesIO is used here.
        from io import BytesIO

        parser.read_file(BytesIO(data))
    except configparser.Error as exc:
        raise ValueError("Invalid INI data") from exc

    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result


def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Deserialize `data_bytes` according to the trusted `format_string`.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data.
    format_string : str
        Identifier of the serialization format ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list).

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Call the corresponding safe decoder
    return ALLOWED_FORMATS[fmt](data_bytes)