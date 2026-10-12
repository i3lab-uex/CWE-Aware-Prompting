import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

# Define the set of trusted formats that are allowed for deserialization.
TRUSTED_FORMATS = {"json", "xml"}

def _parse_xml_element(element: ET.Element) -> Any:
    """
    Recursively convert an XML element tree into a nested dictionary.
    Text content is preserved when there are no child elements.
    """
    # If element has children, convert each child recursively
    if list(element):
        return {
            child.tag: _parse_xml_element(child)
            for child in element
        }
    # If no children, return the text content stripped of whitespace.
    return element.text.strip() if element.text else None

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Convert serialized data back into a Python object.
    
    Parameters
    ----------
    serialized_data : bytes
        The serialized data in byte form.
    format_type : str
        One of the permitted serialized data formats (e.g. 'json', 'xml').
    
    Returns
    -------
    Any
        The deserialized Python object.
    
    Raises
    ------
    ValueError
        If the provided format_type is not in the list of trusted formats.
    """
    if format_type not in TRUSTED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    # Decode the bytes to a string using UTF-8.  This is safe for JSON and XML.
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if format_type == "json":
        # json.loads already performs safety checks; no arbitrary code execution.
        return json.loads(text)

    if format_type == "xml":
        # Parse XML safely.  ElementTree does not execute code, but we convert to a
        # Python structure that is easy to use.
        root = ET.fromstring(text)
        return {root.tag: _parse_xml_element(root)}

    # The check above guarantees we never reach this point, but keep for completeness.
    raise ValueError(f"Unsupported format: {format_type!r}")