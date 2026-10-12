import json
from typing import Any

# The standard library's ElementTree is safe for most cases, but to guard
# against XML external entity attacks we explicitly disallow any DTD or
# external entities by parsing only the string content.
import xml.etree.ElementTree as ET

def _safe_xml_to_dict(elem: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text nodes are returned as strings; child elements become nested dicts or lists.
    """
    # If element has no children, return its text (stripped)
    if len(elem) == 0:
        return elem.text.strip() if elem.text else None

    # Aggregate children by tag name
    result = {}
    for child in elem:
        child_val = _safe_xml_to_dict(child)
        tag = child.tag
        if tag in result:
            # If we already have a list for this tag, append; else convert to list
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_val)
        else:
            result[tag] = child_val
    return result

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize `encoded_data` according to the specified `method`.

    Supported formats: 'json', 'xml'.
    Any other format will raise ValueError.

    Parameters
    ----------
    encoded_data : bytes
        The serialized data.
    method : str
        The serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise TypeError("encoded_data must be bytes-like")

    method = method.lower()
    if method == 'json':
        try:
            # Decode bytes to string using UTF-8; errors='strict' ensures invalid
            # byte sequences raise a UnicodeDecodeError, which we convert to ValueError.
            text = encoded_data.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif method == 'xml':
        try:
            # ElementTree.fromstring is safe against DTDs and external entities
            root = ET.fromstring(encoded_data)
            return _safe_xml_to_dict(root)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    else:
        # Explicitly reject dangerous or unsupported formats (e.g., pickle)
        raise ValueError(f"Unsupported serialization format: {method!r}")