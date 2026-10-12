import json
import configparser
from typing import Any, Dict

# List of formats that are considered safe for deserialization
ALLOWED_FORMATS = {"json", "ini"}


def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize data coming from unreliable sources.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary format.
    format_string : str
        Identifier of the serialization format. Must be one of
        ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object. For 'ini' the result is a dict of
        sections mapping to dicts of key/value pairs.

    Raises
    ------
    ValueError
        If the format_string is not supported or if deserialization fails.
    """
    # Normalize format string to lower case for comparison
    fmt = format_string.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Decode bytes to string; assume UTF‑8, raise if invalid
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data bytes are not valid UTF‑8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dict: {section: {key: value}}
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Should never reach here because of the earlier check
    raise ValueError(f"Unhandled format: {format_string!r}")