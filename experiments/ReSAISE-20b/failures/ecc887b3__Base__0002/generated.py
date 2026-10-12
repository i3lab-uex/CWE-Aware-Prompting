import json
import xml.etree.ElementTree as ET
from typing import Any, Union

def _xml_to_dict(elem: ET.Element) -> dict:
    """Recursively convert an ElementTree element into a dictionary."""
    d = {elem.tag: {} if elem.attrib else None}
    children = list(elem)
    if children:
        dd = {}
        for child in children:
            child_dict = _xml_to_dict(child)
            tag = list(child_dict)[0]
            if tag in dd:
                # If multiple children with same tag, store as list
                if not isinstance(dd[tag], list):
                    dd[tag] = [dd[tag]]
                dd[tag].append(child_dict[tag])
            else:
                dd[tag] = child_dict[tag]
        d[elem.tag] = dd
    if elem.attrib:
        d[elem.tag].update(('@' + k, v) for k, v in elem.attrib.items())
    text = elem.text.strip() if elem.text else ''
    if text:
        d[elem.tag]['#text'] = text
    return d

def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize `serialized_bytes` according to the specified format.
    
    Supported formats:
        - 'json': deserialized using json.loads
        - 'xml' : parsed into an ElementTree element or dictionary representation
    
    Raises:
        ValueError: if the format is not supported or deserialization fails.
    """
    fmt = allowed_format.lower()
    
    if fmt == 'json':
        try:
            return json.loads(serialized_bytes.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc
    
    if fmt == 'xml':
        try:
            elem = ET.fromstring(serialized_bytes)
            # Convert to a dictionary for easier consumption
            return _xml_to_dict(elem)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc
    
    # Add more safe formats here if needed.
    
    raise ValueError(f"Unsupported or unsafe format: {allowed_format}")