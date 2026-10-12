import json
import xml.etree.ElementTree as ET
from typing import Any

def _xml_to_dict(element: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a Python dict.
    Handles only simple XML structures (no attributes or mixed content).
    """
    # If the element has no child elements, return its text
    if len(element) == 0:
        return element.text or ""

    # Build a dictionary from child tags
    result = {}
    for child in element:
        value = _xml_to_dict(child)
        if child.tag in result:
            # If the tag already exists, convert to a list
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(value)
        else:
            result[child.tag] = value
    return result

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using only trusted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data in binary form.
    encoding_type : str
        The serialization format, e.g. 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially unsafe.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    fmt = encoding_type.lower()

    if fmt == "json":
        # JSON is safe and widely supported
        text = byte_data.decode("utf-8")
        return json.loads(text)

    if fmt == "xml":
        # Parse XML safely; only simple structures are supported
        text = byte_data.decode("utf-8")
        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc
        return _xml_to_dict(root)

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or dangerous serialization format: {encoding_type}")