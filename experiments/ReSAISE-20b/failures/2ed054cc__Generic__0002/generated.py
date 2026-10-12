import json
import xml.etree.ElementTree as ET
from typing import Any

__ALLOWED_FORMATS = {"json", "xml"}


def _convert_xml_element_to_dict(elem: ET.Element) -> dict:
    """
    Recursively convert an XML Element into a nested dictionary.
    Text content is stored under the key '#text'.
    Attributes are stored under the key '@attributes'.
    """
    d: dict[str, Any] = {}
    if elem.attrib:
        d["@attributes"] = dict(elem.attrib)

    # Handle child elements
    children = list(elem)
    if children:
        child_dict: dict[str, Any] = {}
        for child in children:
            child_obj = _convert_xml_element_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # If multiple children with same tag, store as list
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_obj)
            else:
                child_dict[tag] = child_obj
        d.update(child_dict)

    # Handle text content
    text = elem.text.strip() if elem.text else ""
    if text:
        d["#text"] = text

    return d


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes `raw_data` according to the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of a Python object.
    serialization_format : str
        One of the supported formats: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in __ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    try:
        if fmt == "json":
            # Decode bytes to string and parse JSON
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "xml":
            # Parse XML into an ElementTree and convert to dict
            root = ET.fromstring(raw_data)
            return {root.tag: _convert_xml_element_to_dict(root)}
    except Exception as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc