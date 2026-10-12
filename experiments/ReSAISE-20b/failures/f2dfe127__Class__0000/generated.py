import json
import xml.etree.ElementTree as ET
from typing import Any

try:
    # PyYAML is optional; if not available, we simply don't support 'yaml'
    import yaml
except ImportError:
    yaml = None


def _parse_xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an XML element into a dictionary.
    Attributes are prefixed with '@', text content is stored under '#text'.
    """
    node: dict = {}
    if element.attrib:
        for k, v in element.attrib.items():
            node[f"@{k}"] = v

    # Process child elements
    children = list(element)
    if children:
        for child in children:
            child_dict = _parse_xml_to_dict(child)
            key = child.tag
            if key in node:
                # If already present, convert to list
                if not isinstance(node[key], list):
                    node[key] = [node[key]]
                node[key].append(child_dict)
            else:
                node[key] = child_dict

    # Text content
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text

    return node


def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `data_bytes` into a Python object based on the provided format.
    
    Supported formats:
        - 'json': JSON format
        - 'yaml': YAML (safe) format, requires PyYAML
        - 'xml' : XML format converted to a nested dictionary
    
    Raises:
        ValueError: If the format is unsupported or dangerous.
        Exception: Any exception raised by the underlying parser (e.g., malformed data).
    """
    if not isinstance(data_bytes, bytes):
        raise TypeError("data_bytes must be a bytes object")

    fmt = format_name.lower()

    if fmt == "json":
        return json.loads(data_bytes.decode("utf-8"))

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (PyYAML missing)")
        return yaml.safe_load(data_bytes.decode("utf-8"))

    if fmt == "xml":
        root = ET.fromstring(data_bytes.decode("utf-8"))
        return {root.tag: _parse_xml_to_dict(root)}

    raise ValueError(f"Unsupported or unsafe format '{format_name}'. "
                     "Allowed formats: 'json', 'yaml' (if PyYAML installed), 'xml'.")