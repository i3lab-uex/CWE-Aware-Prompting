#!/usr/bin/env python3
"""
Secure deserialization utility.

This module provides a single function, `unpack_serialized_object`, which
deserializes binary data only for a pre‑approved set of formats.  Unsupported or
potentially unsafe formats (e.g., pickle) will raise an exception.

The implementation follows best practices for security and handles
common edge cases such as non‑UTF‑8 input or malformed data.
"""

import json
import configparser
from typing import Any, Dict


# Define the whitelist of safe formats.
_SAFE_FORMATS = {"json", "ini"}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data into a Python object for approved formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        The format used for deserialization. Supported values are:
        - 'json': JSON text.
        - 'ini' : INI configuration data.

    Returns
    -------
    Any
        The deserialized Python object.  For 'json', this will be a standard
        Python data structure (dict, list, etc.).  For 'ini', a nested dict
        representing sections and options is returned.

    Raises
    ------
    ValueError
        If `struct_format` is not in the whitelist or if deserialization fails.
    """
    # Normalise format string
    fmt = struct_format.strip().lower()

    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: '{struct_format}'")

    try:
        if fmt == "json":
            # JSON is text; decode bytes to str safely.
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # INI files are parsed into a ConfigParser object; convert to dict.
            parser = configparser.ConfigParser()
            # ConfigParser expects a file‑like object; use BytesIO.
            from io import BytesIO
            parser.read_file(BytesIO(byte_data))
            # Convert to nested dict.
            result: Dict[str, Dict[str, str]] = {
                section: {key: val for key, val in parser.items(section)}
                for section in parser.sections()
            }
            return result

    except Exception as exc:
        # Wrap any exception to provide a clear error message.
        raise ValueError(f"Deserialization failed for format '{struct_format}': {exc}") from exc