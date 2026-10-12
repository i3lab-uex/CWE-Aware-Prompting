import json
import xml.etree.ElementTree as ET
from typing import Any

# Allowed serialization formats (secure only)
ALLOWED_FORMATS = {"json", "xml"}

def _xml_to_dict(element: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a Python dict.
    Text content is preserved when no child elements are present.
    """
    # If element has children, convert each child
    if list(element):
        d = {}
        for child in element:
            child_dict = _xml_to_dict(child)
            tag = child.tag
            if tag in d:
                # If the key already exists, convert to list
                if not isinstance(d[tag], list):
                    d[tag] = [d[tag]]
                d[tag].append(child_dict)
            else:
                d[tag] = child_dict
        return d

    # No children: return text (strip to avoid whitespace-only strings)
    return element.text.strip() if element.text and element.text.strip() else None

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize raw data into a Python object.

    Parameters
    ----------
    raw_data : bytes
        Serialized representation of the data.
    serialization_format : str
        Format used for serialization. Supported formats are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    try:
        if fmt == "json":
            # JSON expects a text string
            decoded = raw_data.decode("utf-8")
            return json.loads(decoded)

        if fmt == "xml":
            # Parse XML into ElementTree and convert to dict
            root = ET.fromstring(raw_data)
            return {root.tag: _xml_to_dict(root)}

    except Exception as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc