import json
from xml.etree import ElementTree as ET
from typing import Any

def _xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a plain dictionary.
    Only text nodes and attributes are preserved. Child elements are
    represented as nested dictionaries or lists when multiple children
    share the same tag.
    """
    node: dict = {}
    # Include attributes if any
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Include text content if present
    text = (element.text or "").strip()
    if text:
        node["#text"] = text

    # Process child elements
    children_by_tag: dict[str, list] = {}
    for child in element:
        children_by_tag.setdefault(child.tag, []).append(_xml_to_dict(child))

    for tag, items in children_by_tag.items():
        if len(items) == 1:
            node[tag] = items[0]
        else:
            node[tag] = items

    return node


def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize *encoded_data* using the specified *method*.

    Supported formats:

        - 'json': JSON data decoded to Python objects.
        - 'xml' : XML data converted into nested dictionaries.

    Any other method raises ValueError to prevent insecure or
    unsupported deserialization.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise TypeError("encoded_data must be bytes or bytearray")

    try:
        text = encoded_data.decode('utf-8')
    except Exception as exc:
        raise ValueError("Data is not valid UTF‑8") from exc

    method = method.lower()
    if method == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == 'xml':
        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc
        return {root.tag: _xml_to_dict(root)}

    raise ValueError(f"Unsupported or dangerous serialization format: {method}")