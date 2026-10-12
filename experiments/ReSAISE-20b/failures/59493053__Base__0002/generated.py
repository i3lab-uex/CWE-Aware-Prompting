import json
import xml.etree.ElementTree as ET

def _xml_to_dict(element):
    """Recursively convert an ElementTree element into a dictionary."""
    node = {}
    # Include attributes
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    # Include text
    text = (element.text or "").strip()
    if text:
        node["#text"] = text
    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_name = child.tag
            child_obj = _xml_to_dict(child)
            if child_name in child_dict:
                # If multiple children with same tag, store as list
                if not isinstance(child_dict[child_name], list):
                    child_dict[child_name] = [child_dict[child_name]]
                child_dict[child_name].append(child_obj)
            else:
                child_dict[child_name] = child_obj
        node.update(child_dict)
    return node

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Deserialize `input_data` based on the specified `serialization_format`.

    Supported formats:
        - 'json': JSON data (UTF‑8 encoded)
        - 'xml' : XML data

    Raises:
        ValueError: If the format is unsupported or potentially dangerous.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            text = input_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            element = ET.fromstring(input_data.decode("utf-8"))
            return _xml_to_dict(element)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow pickle and other potentially dangerous formats
    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")