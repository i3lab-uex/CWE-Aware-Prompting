import json
import xml.etree.ElementTree as ET
from typing import Any


def _xml_to_dict(elem: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Handles attributes and text content in a simple, deterministic way.
    """
    d = {}
    # include element attributes
    if elem.attrib:
        d.update({f"@{k}": v for k, v in elem.attrib.items()})
    # include child elements
    children = list(elem)
    if children:
        for child in children:
            child_dict = _xml_to_dict(child)
            tag = child.tag
            if tag in d:
                # multiple children with same tag -> list
                if not isinstance(d[tag], list):
                    d[tag] = [d[tag]]
                d[tag].append(child_dict)
            else:
                d[tag] = child_dict
    # include text if present and not just whitespace
    text = elem.text.strip() if elem.text else ""
    if text:
        d["#text"] = text
    return d


def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `method_name`.

    Supported formats are:
        * json  - safe JSON deserialization
        * xml   - parsed into a dictionary representation

    Any other format raises ValueError to prevent unsafe deserialization.
    """
    if not isinstance(raw_data, bytes):
        raise TypeError("raw_data must be of type 'bytes'")

    method = method_name.lower()
    if method == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            root = ET.fromstring(raw_data)
            return {root.tag: _xml_to_dict(root)}
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Any other method is considered unsafe or unsupported
    raise ValueError(f"Unsupported deserialization format: {method_name}")