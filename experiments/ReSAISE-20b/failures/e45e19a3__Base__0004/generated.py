import json
import xml.etree.ElementTree as ET
from typing import Any

# A minimal XML-to-dict conversion that only handles simple elements and attributes
def _xml_to_dict(element: ET.Element) -> Any:
    """Recursively convert an ElementTree element into a nested dict."""
    node: dict[str, Any] = {}
    # Add attributes
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Add text if present
    text = (element.text or "").strip()
    if text:
        node["#text"] = text
    # Add child elements
    children = list(element)
    if children:
        child_dict: dict[str, Any] = {}
        for child in children:
            child_obj = _xml_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # If multiple children with same tag, store as list
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_obj)
            else:
                child_dict[tag] = child_obj
        node.update(child_dict)
    return node

def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize a byte sequence into a Python object using only safe formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        The serialization format: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = data_type.lower()
    if fmt == "json":
        # json.loads works with str, so decode using utf-8
        try:
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(input_data)
            return {root.tag: _xml_to_dict(root)}
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Explicitly reject unsafe or unsupported formats
    raise ValueError(f"Unsupported data_type: {data_type!r}. "
                     "Only 'json' and 'xml' are allowed.")