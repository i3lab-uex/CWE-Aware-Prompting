import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

# A small helper to convert an XML element into a Python dictionary.
def _xml_to_dict(elem: ET.Element) -> Dict[str, Any]:
    """Recursively convert an ElementTree element into a dictionary."""
    node: Dict[str, Any] = {}
    # Include attributes if any
    if elem.attrib:
        node.update({f"@{k}": v for k, v in elem.attrib.items()})
    # Process child elements
    children = list(elem)
    if children:
        # Group children by tag name
        child_dict: Dict[str, Any] = {}
        for child in children:
            child_val = _xml_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # Ensure the value is a list when multiple children share the same tag
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_val)
            else:
                child_dict[tag] = child_val
        node.update(child_dict)

    # Include text content if present and not just whitespace
    text = elem.text.strip() if elem.text else ""
    if text:
        node["#text"] = text

    return node


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize raw bytes into a Python object from a trusted format.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte form.
    data_type : str
        The serialization format ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data_type is unsupported or potentially dangerous.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes-like")

    fmt = data_type.lower()
    if fmt == "json":
        try:
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(input_data.decode("utf-8"))
            return {root.tag: _xml_to_dict(root)}
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Reject potentially dangerous or unsupported formats
    raise ValueError(f"Unsupported data type '{data_type}'. Only 'json' and 'xml' are allowed.")