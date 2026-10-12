import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the set of formats that are allowed for safe deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def _element_to_dict(element: ET.Element) -> Any:
    """
    Recursively convert an XML ElementTree into a nested dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    """
    node: dict[str, Any] = {}
    # Handle attributes
    if element.attrib:
        node["@attributes"] = dict(element.attrib)

    # Handle child elements
    children = list(element)
    if children:
        child_dict: dict[str, Any] = {}
        for child in children:
            child_obj = _element_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # If the same tag appears multiple times, store as a list
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_obj)
            else:
                child_dict[tag] = child_obj
        node.update(child_dict)

    # Handle text content
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text

    return node


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize a byte string into a Python object.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte string containing the serialized data.
    allowed_format : str
        One of the supported formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered unsafe.
    """
    fmt = allowed_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format}")

    if fmt == "json":
        try:
            return json.loads(serialized_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(serialized_bytes.decode("utf-8"))
            return _element_to_dict(root)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # The code should never reach here due to the earlier check
    raise ValueError(f"Unhandled format: {allowed_format}")