import json
import xml.etree.ElementTree as ET
from typing import Any

def _xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text content is preserved under the key "__text__".
    Attributes are prefixed with "@".
    """
    node: dict = {}
    if element.attrib:
        for key, value in element.attrib.items():
            node[f"@{key}"] = value
    children = list(element)
    if children:
        child_dict: dict[str, Any] = {}
        for child in children:
            child_obj = _xml_to_dict(child)
            if child.tag not in child_dict:
                child_dict[child.tag] = [child_obj]
            else:
                child_dict[child.tag].append(child_obj)
        node.update(child_dict)
    text = element.text
    if text and text.strip():
        node["__text__"] = text.strip()
    return node

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize data from raw bytes into a Python object.
    
    Only the following formats are allowed:
      - json
      - xml
    
    Parameters
    ----------
    data_bytes : bytes
        Serialized object in byte format.
    format_name : str
        Serialization format (e.g., 'json', 'xml').
    
    Returns
    -------
    Any
        Deserialized Python object.
    
    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be bytes or bytearray")

    fmt = format_name.lower()
    if fmt == "json":
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    if fmt == "xml":
        try:
            element = ET.fromstring(data_bytes)
        except ET.ParseError as exc:
            raise ValueError("Malformed XML data") from exc
        return _xml_to_dict(element)

    # Any other format is considered unsafe or unsupported.
    raise ValueError(f"Unsupported or potentially dangerous format: {format_name}")