#!/usr/bin/env python3
"""
Secure deserialization of byte‑encoded data from trusted formats only.
Supported formats: JSON, XML (defusedxml).  All other formats are rejected.

CWE-913: Prevents accidental execution of malicious code by rejecting
pickle and other unsafe serialization mechanisms.
"""

from __future__ import annotations

import json
from typing import Any, Union

# Use defusedxml to avoid XML external entity attacks
try:
    from defusedxml import ElementTree as DefusedElementTree
except ImportError:
    # If defusedxml is not installed, fall back to the standard library
    # but issue a warning that XML parsing may be unsafe.
    import warnings

    from xml.etree import ElementTree as DefusedElementTree
    warnings.warn(
        "defusedxml is not installed; XML parsing may be unsafe.",
        RuntimeWarning,
    )


def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize *encoded_data* according to the specified *method*.

    Parameters
    ----------
    encoded_data : bytes
        The serialized data in byte format.
    method : str
        The serialization format used: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *method* is unsupported or considered dangerous.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise ValueError("encoded_data must be bytes or bytearray")

    method = method.lower()
    if method == "json":
        try:
            # Decode bytes to string using UTF-8 (common for JSON)
            text = encoded_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == "xml":
        try:
            # Parse XML securely with defusedxml
            root = DefusedElementTree.fromstring(encoded_data)
        except (DefusedElementTree.ParseError, Exception) as exc:
            raise ValueError("Invalid or unsafe XML data") from exc

        # Convert ElementTree to a nested dictionary for easier use.
        def _elem_to_dict(elem: DefusedElementTree.Element) -> Union[dict, str]:
            # If element has no children and no attributes, return its text
            if not list(elem) and not elem.attrib:
                return elem.text or ""

            d: dict[str, Any] = {}
            # Add attributes
            for key, value in elem.attrib.items():
                d[f"@{key}"] = value

            # Add child elements
            for child in elem:
                child_dict = _elem_to_dict(child)
                tag = child.tag
                if tag in d:
                    # Convert to list if multiple children with same tag
                    if not isinstance(d[tag], list):
                        d[tag] = [d[tag]]
                    d[tag].append(child_dict)
                else:
                    d[tag] = child_dict

            # Add text if present
            if elem.text and elem.text.strip():
                d["#text"] = elem.text.strip()

            return d

        return {root.tag: _elem_to_dict(root)}

    else:
        # Explicitly disallow pickle and any other format
        raise ValueError(f"Unsupported or dangerous serialization method: {method}")


# Example usage (for manual testing)
if __name__ == "__main__":
    json_bytes = b'{"key": "value", "number": 42}'
    print(decode_serialized_data(json_bytes, "json"))

    xml_bytes = b"""<?xml version="1.0"?>
<root>
    <child name="first">Hello</child>
    <child name="second">World</child>
</root>"""
    print(decode_serialized_data(xml_bytes, "xml"))