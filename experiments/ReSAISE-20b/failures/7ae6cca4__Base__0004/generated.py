import json
import configparser
from typing import Any

# Define the set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format identifier.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or not in the allowed list.
    json.JSONDecodeError
        If JSON decoding fails.
    configparser.Error
        If INI parsing fails.
    """
    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Decode bytes to string using UTF-8; errors='strict' will raise UnicodeDecodeError on failure.
    text = data_bytes.decode("utf-8")

    if fmt == "json":
        # json.loads is safe for basic data types (dict, list, str, int, float, bool, None).
        return json.loads(text)

    if fmt == "ini":
        # Parse INI into a nested dictionary structure.
        parser = configparser.ConfigParser()
        # configparser expects file-like object; use read_string.
        parser.read_string(text)
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled format: {format_string!r}")