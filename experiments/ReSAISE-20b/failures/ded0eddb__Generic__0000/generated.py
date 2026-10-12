#!/usr/bin/env python3
"""
Utility to safely deserialize data from raw bytes.

Supported formats:
- json: decoded using the standard `json` module.
- xml: parsed into an ElementTree.Element; entity expansion is disabled.

Unsupported or unsafe formats (e.g., pickle, yaml) raise ValueError.
"""

import json
from xml.etree import ElementTree as ET
from typing import Any


# Whitelist of allowed formats
_ALLOWED_FORMATS = {"json", "xml"}


def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Deserialize *bytes_data* according to *data_format*.

    Parameters
    ----------
    bytes_data : bytes
        Raw serialized data.
    data_format : str
        Serialization format. Must be one of the allowed formats.

    Returns
    -------
    Any
        The deserialized Python object. For XML, an ElementTree.Element is returned.

    Raises
    ------
    ValueError
        If *data_format* is not in the whitelist or if deserialization fails.
    """
    fmt = data_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    try:
        if fmt == "json":
            # Decode bytes to str using UTF-8 (common for JSON)
            text = bytes_data.decode("utf-8")
            return json.loads(text)

        if fmt == "xml":
            # Parse XML safely; ElementTree handles UTF-8 by default
            return ET.fromstring(bytes_data)

    except Exception as exc:
        # Wrap any exception in ValueError to keep the API consistent
        raise ValueError(f"Failed to deserialize data as {data_format}: {exc}") from exc