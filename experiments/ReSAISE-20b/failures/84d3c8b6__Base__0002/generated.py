import json
from typing import Any

# defusedxml provides a safe XML parser that mitigates common attacks.
# It is part of the standard library as of Python 3.9, otherwise install via pip.
try:
    from defusedxml import ElementTree as ET
except ImportError:  # pragma: no cover - defensive fallback
    import xml.etree.ElementTree as ET


def _decode_json(data: bytes) -> Any:
    """
    Decode JSON data safely.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise ValueError("JSON data must be UTF‑8 encoded") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Invalid JSON data") from exc


def _decode_xml(data: bytes) -> ET.Element:
    """
    Decode XML data safely using defusedxml.
    Returns the root ElementTree element.
    """
    try:
        # defusedxml's ElementTree.fromstring is safe against XML attacks
        return ET.fromstring(data)
    except ET.ParseError as exc:  # pragma: no cover
        raise ValueError("Invalid XML data") from exc


def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize *encoded_data* using the specified *method*.

    Supported formats are:
        - 'json': JSON text encoded as UTF‑8 bytes.
        - 'xml' : XML data; returned as an ElementTree.Element.

    Unsupported or dangerous formats raise ValueError.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise TypeError("encoded_data must be bytes or bytearray")

    method = method.lower()
    if method == "json":
        return _decode_json(encoded_data)
    elif method == "xml":
        return _decode_xml(encoded_data)
    else:
        raise ValueError(f"Unsupported or dangerous serialization method: {method!r}")