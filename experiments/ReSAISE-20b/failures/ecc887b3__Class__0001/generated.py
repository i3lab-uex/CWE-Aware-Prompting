import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

# List of formats that are considered safe for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def _element_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an XML element and its children into a dictionary.
    Text content is preserved as the value of the 'text' key if present.
    """
    node: Dict[str, Any] = {}
    # Attributes
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Child elements
    children = list(element)
    if children:
        child_dict: Dict[str, Any] = {}
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
    # Text content
    text = element.text.strip() if element.text else ""
    if text:
        node["text"] = text
    return node

def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize a byte string into a Python object, using only
    formats that are explicitly allowed.

    Parameters:
        serialized_bytes (bytes): The raw bytes representing the serialized data.
        allowed_format (str): Identifier of the serialization format
                              ('json', 'xml').

    Returns:
        Any: The deserialized Python object (e.g., dict, list).

    Raises:
        ValueError: If the format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format}")

    try:
        if fmt == "json":
            # JSON expects a text string; decode using UTF-8
            decoded = serialized_bytes.decode("utf-8")
            return json.loads(decoded)
        elif fmt == "xml":
            # XML parsing
            root = ET.fromstring(serialized_bytes)
            return {root.tag: _element_to_dict(root)}
    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        raise ValueError(f"Deserialization failed for format '{allowed_format}': {exc}") from exc