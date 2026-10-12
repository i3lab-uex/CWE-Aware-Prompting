#!/usr/bin/env python3
"""
Utility for safely deserializing binary data from external sources.
Only a whitelisted set of formats is supported to mitigate
CWE‑502 (Deserialization of Untrusted Data).
"""

import json
import configparser
from typing import Any, Dict

# Whitelisted formats and their corresponding deserialization functions.
def _deserialize_json(data: bytes) -> Any:
    """Deserialize JSON data from bytes."""
    # Decode using UTF‑8 and parse with the standard library json module.
    return json.loads(data.decode("utf-8"))

def _deserialize_ini(data: bytes) -> Dict[str, Any]:
    """Deserialize INI data from bytes."""
    parser = configparser.ConfigParser()
    # ConfigParser expects a file-like object; we provide one using BytesIO.
    from io import StringIO
    parser.read_file(StringIO(data.decode("utf-8")))
    # Convert the ConfigParser object into a plain dictionary.
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result

# Map of allowed format names to deserialization functions.
_ALLOWED_FORMATS = {
    "json": _deserialize_json,
    "ini": _deserialize_ini,
}

def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Deserialize binary data using a safe, whitelisted method.

    Parameters
    ----------
    data_input : bytes
        The raw serialized data received from an external source.
    format_type : str
        Identifier of the serialization format. Allowed values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the allowed list or if deserialization fails.
    """
    # Normalize the format string to lowercase for case‑insensitive matching.
    fmt = format_type.strip().lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or disallowed format '{format_type}'. "
            "Allowed formats: 'json', 'ini'."
        )

    # Attempt to deserialize; propagate any exception as ValueError.
    try:
        return _ALLOWED_FORMATS[fmt](data_input)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Deserialization failed for format '{format_type}': {exc}") from exc