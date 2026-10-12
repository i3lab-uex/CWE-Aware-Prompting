import json
import xml.etree.ElementTree as ET
from typing import Any

def _xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    This is a simple implementation suitable for basic XML structures
    and avoids executing any code from the XML.
    """
    node = {}
    # Include element attributes if present
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Process child elements
    children = list(element)
    if children:
        for child in children:
            child_dict = _xml_to_dict(child)
            tag = child.tag
            if tag in node:
                # Existing key, convert to list
                if not isinstance(node[tag], list):
                    node[tag] = [node[tag]]
                node[tag].append(child_dict)
            else:
                node[tag] = child_dict
    # Include text content if present and non-whitespace
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text
    return node

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using only
    trusted serialization formats.

    Parameters:
        byte_data (bytes): Serialized data.
        encoding_type (str): Serialization format identifier
                             ('json' or 'xml').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the encoding_type is unsupported or
                    considered unsafe.
        json.JSONDecodeError / ET.ParseError: If the data is malformed.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    # Normalize the encoding_type string
    fmt = encoding_type.strip().lower()

    if fmt == "json":
        # JSON is safe for deserialization
        return json.loads(byte_data.decode("utf-8"))

    if fmt == "xml":
        # Parse XML into a dictionary; no code execution occurs
        root = ET.fromstring(byte_data.decode("utf-8"))
        return {root.tag: _xml_to_dict(root)}

    # Any other format is disallowed to avoid unsafe deserialization
    raise ValueError(f"Unsupported or dangerous serialization format: '{encoding_type}'")