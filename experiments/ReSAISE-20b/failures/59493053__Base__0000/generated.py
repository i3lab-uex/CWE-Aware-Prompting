#!/usr/bin/env python3
"""
Secure deserialization helper.

This module implements :func:`deserialize_data`, which safely converts a byte
stream into a Python object for a limited set of formats.  The function is
designed to mitigate CWE‑502 (Deserialization of Untrusted Data) by rejecting
dangerous formats such as ``pickle`` and limiting the parsing logic to safe
standard libraries.

Supported formats:
    * json  – decoded with :mod:`json` (only basic types: dict, list,
      str, int, float, bool, None)
    * xml   – parsed with :mod:`xml.etree.ElementTree`.  The returned object
      is an ``Element`` instance representing the root element.
"""

import json
import xml.etree.ElementTree as ET
from typing import Any

__all__ = ["deserialize_data"]

# A whitelist of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "xml"}


def _parse_json(data: bytes) -> Any:
    """Parse JSON data from bytes, ensuring it is UTF‑8 encoded."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data must be UTF‑8 encoded") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _parse_xml(data: bytes) -> ET.Element:
    """Parse XML data from bytes, using ElementTree."""
    try:
        # Parse directly from bytes to avoid intermediate string conversion.
        return ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data") from exc


def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize *input_data* according to the specified
    *serialization_format*.

    Parameters
    ----------
    input_data : bytes
        The serialized data to deserialize.
    serialization_format : str
        One of the supported formats: ``'json'`` or ``'xml'``.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or the data is malformed.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise ValueError("input_data must be bytes or bytearray")

    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {serialization_format}")

    if fmt == "json":
        return _parse_json(input_data)
    # fmt == "xml"
    return _parse_xml(input_data)


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     sample_json = b'{"key": "value", "list": [1, 2, 3]}'
#     print(deserialize_data(sample_json, "json"))
#
#     sample_xml = b"<root><child>text</child></root>"
#     root_elem = deserialize_data(sample_xml, "xml")
#     print(ET.tostring(root_elem).decode())