import json
import xml.etree.ElementTree as ET
from typing import Any

def _parse_xml_element(element: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a Python dict/list.
    Only attributes, text and child elements are preserved.
    """
    # If element has no children and only text
    if not list(element) and (element.text is None or element.text.strip() == ""):
        return {}
    # Convert children
    result = {}
    for child in element:
        key = child.tag
        value = _parse_xml_element(child)
        # Handle multiple children with same tag as list
        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    # Include text if present and not just whitespace
    text = element.text.strip() if element.text else ""
    if text:
        result["_text"] = text
    return result

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Safely deserialize data from the given format.

    Parameters
    ----------
    encoded_data : bytes
        Serialized object in byte form.
    method : str
        Serialization format: 'json', 'xml' or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially dangerous.
    """
    method = method.lower()
    if method == "json":
        try:
            text = encoded_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            text = encoded_data.decode("utf-8")
            root = ET.fromstring(text)
            return _parse_xml_element(root)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    if method == "pickle":
        # Pickle is explicitly disallowed due to security risks
        raise ValueError("Deserialization of pickle data is prohibited")

    # Any other format is unsupported
    raise ValueError(f"Unsupported serialization method: {method}")