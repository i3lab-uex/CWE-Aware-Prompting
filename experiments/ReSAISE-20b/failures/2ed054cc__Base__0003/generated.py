import json
import xml.etree.ElementTree as ET
from typing import Any, Dict


def _xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text content is preserved, attributes are included under the key '@attributes',
    and child elements become nested dictionaries or lists when repeated.
    """
    node: Dict[str, Any] = {}
    # Handle attributes
    if element.attrib:
        node["@attributes"] = dict(element.attrib)

    # Handle child elements
    children = list(element)
    if children:
        child_dict: Dict[str, Any] = {}
        for child in children:
            child_name = child.tag
            child_value = _xml_to_dict(child)
            if child_name in child_dict:
                # Existing key -> convert to list
                if not isinstance(child_dict[child_name], list):
                    child_dict[child_name] = [child_dict[child_name]]
                child_dict[child_name].append(child_value)
            else:
                child_dict[child_name] = child_value
        node.update(child_dict)

    # Handle text content
    text = element.text.strip() if element.text else ""
    if text and not children:
        node["#text"] = text
    elif text:
        # If there are both children and text, keep text under a special key
        node["#text"] = text

    return node


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes `raw_data` according to the specified `serialization_format`.
    Only 'json' and 'xml' formats are supported. Unsupported formats raise ValueError.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    serialization_format : str
        One of 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    if not isinstance(raw_data, bytes):
        raise ValueError("raw_data must be of type 'bytes'")

    fmt = serialization_format.lower()
    if fmt == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(raw_data.decode("utf-8"))
            return _xml_to_dict(root)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow any other format (e.g., pickle, yaml, etc.)
    raise ValueError(f"Unsupported serialization format: {serialization_format}")