import json
import configparser
from typing import Any, Dict

# ----------------------------------------------------------------------
# Safe deserialization helper
# ----------------------------------------------------------------------


def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data from a bytes object.

    The data is first decoded using UTF‑8, then parsed with json.loads.
    """
    text = data.decode("utf-8")
    return json.loads(text)


def _deserialize_ini(data: bytes) -> Dict[str, Dict[str, str]]:
    """
    Deserialize INI data from a bytes object.

    The data is decoded using UTF‑8 and parsed with configparser.
    The result is returned as a nested dictionary: {section: {option: value}}.
    """
    text = data.decode("utf-8")
    parser = configparser.ConfigParser()
    # Preserve case for section names and keys
    parser.optionxform = str
    parser.read_string(text)

    result: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        items = dict(parser.items(section))
        result[section] = items
    return result


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------


def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Deserialize binary data using a safe, curated set of formats.

    Parameters
    ----------
    bin_data : bytes
        The binary representation of the serialized data.
    format_type : str
        One of: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_type is unsupported or considered unsafe.
    """
    fmt = format_type.lower()
    if fmt == "json":
        return _deserialize_json(bin_data)
    elif fmt == "ini":
        return _deserialize_ini(bin_data)

    # Any other format is explicitly disallowed
    raise ValueError(
        f"Unsupported or unsafe deserialization format: {format_type!r}"
    )