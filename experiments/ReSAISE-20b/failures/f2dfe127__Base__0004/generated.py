import json
import xml.etree.ElementTree as ET
from typing import Any

def _xml_to_dict(element: ET.Element) -> dict:
    """Recursively convert an ElementTree element into a dictionary."""
    d = {element.tag: {} if element.attrib or list(element) else None}
    if element.text and element.text.strip():
        d[element.tag] = element.text.strip()
    for key, value in element.attrib.items():
        d[element.tag].setdefault("@attributes", {})[key] = value
    for child in element:
        child_dict = _xml_to_dict(child)
        tag, content = next(iter(child_dict.items()))
        if tag in d[element.tag]:
            # Convert to list if multiple children with same tag
            if not isinstance(d[element.tag][tag], list):
                d[element.tag][tag] = [d[element.tag][tag]]
            d[element.tag][tag].append(content)
        else:
            d[element.tag][tag] = content
    return d

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize data from raw bytes into Python objects.

    Parameters
    ----------
    data_bytes : bytes
        Serialized object in byte format.
    format_name : str
        Serialization format (e.g., 'json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    # Normalize format name
    fmt = format_name.strip().lower()

    if fmt == "json":
        try:
            text = data_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(data_bytes)
            return _xml_to_dict(root)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Extend with other safe formats if desired, e.g. yaml.safe_load
    raise ValueError(f"Unsupported or unsafe format: {format_name}")