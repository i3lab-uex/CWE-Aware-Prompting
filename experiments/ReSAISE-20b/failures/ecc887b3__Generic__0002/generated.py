import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def _xml_to_dict(elem: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a Python dictionary.
    Text content is returned as string; children are converted to dicts or lists.
    """
    # If the element has no children, return its text (or empty string if None)
    if len(elem) == 0:
        return elem.text or ""

    # If the element has children, convert each child
    result = {}
    for child in elem:
        child_value = _xml_to_dict(child)
        tag = child.tag

        # Handle repeated tags by storing them in a list
        if tag in result:
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_value)
        else:
            result[tag] = child_value

    return result


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize a byte string into a Python object based on the specified format.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw serialized data.
    allowed_format : str
        The format used for serialization (e.g., 'json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object (dict, list, etc.).

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    try:
        if fmt == "json":
            # Decode bytes to string assuming UTF-8 encoding
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)

        if fmt == "xml":
            # Parse XML and convert to dict
            root = ET.fromstring(serialized_bytes)
            return {root.tag: _xml_to_dict(root)}

    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data as {allowed_format}: {exc}") from exc