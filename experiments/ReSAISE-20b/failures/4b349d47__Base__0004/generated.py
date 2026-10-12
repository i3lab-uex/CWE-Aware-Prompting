import json
import xml.etree.ElementTree as ET
from typing import Any, Dict


def _xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an XML element into a dictionary.
    Attributes are prefixed with '@' to distinguish them from child elements.
    Text content is stored under the key '#text'.
    """
    node: Dict[str, Any] = {}

    # Handle attributes
    for key, value in element.attrib.items():
        node[f"@{key}"] = value

    # Handle child elements
    children: Dict[str, Any] = {}
    for child in element:
        child_dict = _xml_to_dict(child)
        tag = child.tag
        if tag in children:
            # If we already have this tag, convert to a list
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    node.update(children)

    # Handle text
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text

    return node


def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize `serialized_data` according to the specified `format_type`.
    Only 'json' and 'xml' formats are trusted. All other formats raise a ValueError.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte representation of the serialized object.
    format_type : str
        The serialization format ('json' or 'xml').

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list, etc.).

    Raises
    ------
    ValueError
        If `format_type` is not in the allowed set of formats.
    """
    allowed_formats = {"json", "xml"}

    if format_type not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    if format_type == "json":
        # Decode bytes to string using UTF-8, then parse JSON
        return json.loads(serialized_data.decode("utf-8"))

    if format_type == "xml":
        # Parse XML and convert to a nested dictionary
        root = ET.fromstring(serialized_data)
        return {root.tag: _xml_to_dict(root)}

    # This point should never be reached due to the allowed_formats check
    raise ValueError(f"Unhandled format: {format_type!r}")