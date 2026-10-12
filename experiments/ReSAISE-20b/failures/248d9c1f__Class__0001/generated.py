import json
import xml.etree.ElementTree as ET
from typing import Any


def _xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text content is stripped of whitespace; empty elements become None.
    """
    def _convert(el):
        # Handle attributes
        data = {f"@{k}": v for k, v in el.attrib.items()}

        # Handle child elements
        children = list(el)
        if children:
            child_dict = {}
            for child in children:
                child_data = _convert(child)
                tag = child.tag
                if tag in child_dict:
                    # If multiple children share the same tag, store as list
                    if not isinstance(child_dict[tag], list):
                        child_dict[tag] = [child_dict[tag]]
                    child_dict[tag].append(child_data)
                else:
                    child_dict[tag] = child_data
            data.update(child_dict)
        # Handle text content
        text = el.text.strip() if el.text else ''
        if text and not children:
            data['#text'] = text
        return data

    return {element.tag: _convert(element)}


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize `byte_data` into a Python object according to the specified
    `encoding_type`. Only safe, trusted formats are supported.

    Parameters:
        byte_data (bytes): Serialized data in bytes.
        encoding_type (str): Serialization format ('json' or 'xml').

    Returns:
        The deserialized Python object (dict, list, str, etc.).

    Raises:
        ValueError: If the encoding_type is unsupported or dangerous.
        TypeError: If byte_data is not of type bytes.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    encoding_type = encoding_type.lower()
    if encoding_type == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if encoding_type == "xml":
        try:
            root = ET.fromstring(byte_data)
            return _xml_to_dict(root)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Reject any other format (e.g., pickle, marshal, etc.)
    raise ValueError(f"Unsupported or unsafe encoding type: {encoding_type}")