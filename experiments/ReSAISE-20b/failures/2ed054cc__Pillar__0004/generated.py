import json
import xml.etree.ElementTree as ET
from typing import Any

# Whitelisted safe formats
_SAFE_FORMATS = {"json", "xml"}


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely convert serialized data (bytes) into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of the data.
    serialization_format : str
        The format used for serialization. Supported values are
        'json' and 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    try:
        # Decode bytes to text for JSON/XML parsing
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8 encoded text") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON") from exc

    # fmt == "xml"
    try:
        root = ET.fromstring(text)
        return _etree_to_dict(root)
    except ET.ParseError as exc:
        raise ValueError("Failed to parse XML") from exc


def _etree_to_dict(element: ET.Element) -> dict:
    """
    Convert an ElementTree element into a dictionary representation.
    This is a simple implementation that does not preserve all XML nuances
    but provides a safe and predictable structure for typical data.
    """
    node: dict = {}
    # Include attributes
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Include text if present
    text = (element.text or "").strip()
    if text:
        node["#text"] = text
    # Process child elements recursively
    children = list(element)
    if children:
        child_dict: dict[str, Any] = {}
        for child in children:
            child_obj = _etree_to_dict(child)
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