import json
import configparser
from typing import Any, Dict

# Whitelisted formats for safe deserialization
_SAFE_FORMATS = {
    "json": _deserialize_json,
    "ini": _deserialize_ini,
}

def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using a safe, whitelisted format.

    Parameters
    ----------
    byte_data : bytes
        Binary representation of the serialized object.
    struct_format : str
        Format identifier used for deserialization (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or if deserialization fails.
    """
    # Normalise format string
    fmt = struct_format.strip().lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    # Call the appropriate deserializer
    return _SAFE_FORMATS[fmt](byte_data)


def _deserialize_json(byte_data: bytes) -> Any:
    """
    Deserialize JSON data. The input is decoded using UTF-8 with strict error handling.
    """
    try:
        text = byte_data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid UTF-8 data for JSON") from exc

    # Use json.loads with strict mode (default). No object_hook to avoid custom classes.
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON data") from exc


def _deserialize_ini(byte_data: bytes) -> Dict[str, Dict[str, str]]:
    """
    Deserialize INI data into a nested dictionary. Sections and keys are kept as strings.
    """
    try:
        text = byte_data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Invalid UTF-8 data for INI") from exc

    parser = configparser.ConfigParser()
    # Prevent interpolation of values which could lead to code execution
    parser._interpolation = configparser.BasicInterpolation()
    try:
        parser.read_string(text)
    except configparser.Error as exc:
        raise ValueError("Malformed INI data") from exc

    # Convert to a plain dict
    result: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result