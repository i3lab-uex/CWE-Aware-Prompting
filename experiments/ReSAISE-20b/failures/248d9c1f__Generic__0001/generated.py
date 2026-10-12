import json
import xml.etree.ElementTree as ET
from typing import Any


def _xml_to_dict(element: ET.Element) -> Any:
    """Recursively convert an ElementTree element into a dictionary."""
    if len(element) == 0:  # No child elements
        text = element.text.strip() if element.text else None
        return text or {}

    result: dict[str, Any] = {}
    for child in element:
        child_dict = _xml_to_dict(child)
        tag = child.tag
        if tag in result:
            # Existing key, convert to list or append
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_dict)
        else:
            result[tag] = child_dict
    return result


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object based on the specified encoding type.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    encoding_type : str
        Serialization format ('json' or 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the encoding_type is unsupported or potentially dangerous.
    """
    allowed_formats = {"json", "xml"}
    if encoding_type not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe serialization format: {encoding_type}")

    if encoding_type == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if encoding_type == "xml":
        try:
            root = ET.fromstring(byte_data.decode("utf-8"))
            return _xml_to_dict(root)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc