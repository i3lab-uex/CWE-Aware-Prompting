import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

def _xml_to_dict(elem: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an XML element and its children into a dictionary.
    Text content is stored under the key '#text'.
    Attributes are prefixed with '@' to avoid collision.
    """
    node: Dict[str, Any] = {}
    # Add attributes
    for key, value in elem.attrib.items():
        node[f"@{key}"] = value

    # Add child elements
    children: Dict[str, Any] = {}
    for child in elem:
        child_dict = _xml_to_dict(child)
        tag = child.tag
        if tag in children:
            # Ensure multiple tags become a list
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    node.update(children)

    # Add text content if present
    text = elem.text.strip() if elem.text else ""
    if text:
        node["#text"] = text

    return node


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize `input_data` from the specified `data_type`.

    Supported formats: 'json', 'xml'.
    Any other format raises ValueError.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        The serialization format, e.g. 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_type` is not in the set of supported formats.
    """
    if data_type.lower() == "json":
        # Decode bytes to string using UTF-8; ignore errors to avoid crashes
        json_str = input_data.decode("utf-8", errors="strict")
        return json.loads(json_str)

    if data_type.lower() == "xml":
        # Parse XML safely; ElementTree handles well‑formedness
        root = ET.fromstring(input_data)
        return _xml_to_dict(root)

    raise ValueError(f"Unsupported or unsafe deserialization format: {data_type}")