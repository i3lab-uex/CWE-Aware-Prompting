import json
import xml.etree.ElementTree as ET
from typing import Any

# Whitelisted safe formats
SAFE_FORMATS = {"json", "xml"}

def _convert_xml_element(elem: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a Python dict.
    Text content is returned directly if the element has no children,
    otherwise its children are converted to a dict.
    """
    # If the element has no child elements, return its text (trimmed)
    if len(elem) == 0:
        return elem.text.strip() if elem.text else None

    # Build a dict of child elements
    result = {}
    for child in elem:
        key = child.tag
        value = _convert_xml_element(child)

        # Handle repeated tags by storing them in a list
        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    return result

def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize a byte string into a Python object, only if the
    specified format is in the whitelist of safe formats.

    Parameters:
        serialized_bytes (bytes): The raw bytes to deserialize.
        allowed_format (str): The format used for serialization
                              ('json' or 'xml').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is not supported or unsafe.
        json.JSONDecodeError / ET.ParseError: Propagated from the
                                               underlying parser if
                                               input data is malformed.
    """
    fmt = allowed_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format}")

    if fmt == "json":
        # Decode bytes to string using UTF-8 before parsing
        return json.loads(serialized_bytes.decode("utf-8"))

    if fmt == "xml":
        # Parse XML and convert to a dict
        root = ET.fromstring(serialized_bytes.decode("utf-8"))
        return {root.tag: _convert_xml_element(root)}

    # The code should never reach here because of the whitelist
    raise ValueError(f"Unhandled format: {allowed_format}")