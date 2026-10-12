#!/usr/bin/env python3
"""
Secure deserialization of untrusted byte streams.

Supported formats: JSON and XML.  Other formats are rejected to avoid
CWE‑502 (Deserialization of Untrusted Data).
"""

import json
from typing import Any

# Use defusedxml to guard against XML External Entity (XXE) attacks.
try:
    from defusedxml import ElementTree as ET
except ImportError:  # pragma: no cover
    # Fallback to standard library ElementTree with limited safety.
    import xml.etree.ElementTree as ET  # type: ignore

__all__ = ["decode_serialized_data"]


def _parse_json(data_bytes: bytes) -> Any:
    """Parse JSON data from bytes, ensuring UTF‑8 decoding."""
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise ValueError("JSON payload is not valid UTF-8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Invalid JSON data") from exc


def _parse_xml(data_bytes: bytes) -> Any:
    """Parse XML data safely using defusedxml."""
    try:
        root = ET.fromstring(data_bytes)
    except ET.ParseError as exc:  # pragma: no cover
        raise ValueError("Invalid XML data") from exc

    def _elem_to_dict(elem):
        """Recursively convert an ElementTree element to a dict."""
        d = {elem.tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = {}
            for child in children:
                dd.update(_elem_to_dict(child))
            d[elem.tag] = dd
        if elem.attrib:
            d[elem.tag].update(("@" + k, v) for k, v in elem.attrib.items())
        text = elem.text.strip() if elem.text else ""
        if text:
            d[elem.tag]["#text"] = text
        return d

    return _elem_to_dict(root)


def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize *encoded_data* according to *method*.

    Parameters
    ----------
    encoded_data : bytes
        The serialized data in byte form.
    method : str
        Serialization format. Supported values are 'json' and 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *method* is unsupported or the data cannot be parsed.
    """
    method = method.lower()
    if method == "json":
        return _parse_json(encoded_data)
    elif method == "xml":
        return _parse_xml(encoded_data)
    else:
        raise ValueError(f"Unsupported or dangerous serialization method: {method}")