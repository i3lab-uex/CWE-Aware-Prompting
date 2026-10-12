import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "xml"}


def _parse_xml(element: ET.Element) -> Any:
    """
    Recursively convert an XML element into native Python types.
    Only handles simple structures: dictionaries for elements with children
    and strings for leaf nodes. Attributes are ignored to avoid accidental
    injection of arbitrary data.
    """
    # If the element has no children, return its text (or empty string if None)
    if len(element) == 0:
        return element.text or ""

    # Otherwise, build a dict mapping tag names to child values.
    result = {}
    for child in element:
        # If multiple children have the same tag, store them as a list.
        key = child.tag
        value = _parse_xml(child)
        if key in result:
            # Existing entry: convert to list or append
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    return result


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using only trusted formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in byte format.
    encoding_type : str
        The serialization format (e.g., 'json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the encoding_type is unsupported or considered dangerous.
    """
    if not isinstance(encoding_type, str):
        raise ValueError("encoding_type must be a string")

    fmt = encoding_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {encoding_type}")

    # Decode bytes to string for text-based formats
    try:
        decoded = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF-8") from exc

    if fmt == "json":
        # json.loads safely handles primitives, lists, dicts.
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(decoded)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc
        return _parse_xml(root)

    # This point should never be reached due to the ALLOWED_FORMATS check
    raise ValueError(f"Unhandled format: {encoding_type}")