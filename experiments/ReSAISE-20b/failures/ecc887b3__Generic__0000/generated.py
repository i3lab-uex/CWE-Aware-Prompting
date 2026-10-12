import json
import xml.etree.ElementTree as ET
from typing import Any


def _xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    Child elements are grouped by tag name. If multiple children share the same tag,
    they are stored as a list.
    """
    node: dict = {}
    if element.attrib:
        node["@attributes"] = element.attrib

    # Text content
    text = (element.text or "").strip()
    if text:
        node["#text"] = text

    # Process children
    child_map: dict[str, Any] = {}
    for child in element:
        child_dict = _xml_to_dict(child)
        tag = child.tag
        if tag in child_map:
            # Existing entry, convert to list or append
            existing = child_map[tag]
            if isinstance(existing, list):
                existing.append(child_dict)
            else:
                child_map[tag] = [existing, child_dict]
        else:
            child_map[tag] = child_dict

    node.update(child_map)
    return node


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize data from a byte string based on the specified format.

    Supported formats:
        - 'json': JSON text encoded in UTF‑8.
        - 'xml' : XML text encoded in UTF‑8.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw serialized data.
    allowed_format : str
        Format identifier ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt == "json":
        try:
            # json.loads expects a str, so decode UTF‑8 first
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if fmt == "xml":
        try:
            text = serialized_bytes.decode("utf-8")
            root = ET.fromstring(text)
            return _xml_to_dict(root)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Failed to deserialize XML data") from exc

    # Unsupported format
    raise ValueError(f"Unsupported or unsafe deserialization format: {allowed_format}")