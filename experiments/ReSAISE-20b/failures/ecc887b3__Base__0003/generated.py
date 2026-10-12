import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def _convert_xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a nested dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    Child elements are added as lists (if multiple) or single items.
    """
    node: dict = {}
    # Attributes
    if element.attrib:
        node["@attributes"] = element.attrib

    # Text content
    text = (element.text or "").strip()
    if text:
        node["#text"] = text

    # Children
    children: dict[str, Any] = {}
    for child in element:
        child_dict = _convert_xml_to_dict(child)
        tag = child.tag
        if tag in children:
            # Ensure the entry is a list
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    node.update(children)
    return node


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize `serialized_bytes` according to the specified
    `allowed_format`. Only formats listed in ALLOWED_FORMATS are permitted.

    Parameters:
        serialized_bytes (bytes): The raw serialized data.
        allowed_format (str): Format identifier ('json', 'xml').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    # Decode bytes to string safely
    try:
        text = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes are not valid UTF-8") from exc

    try:
        if fmt == "json":
            return json.loads(text)
        elif fmt == "xml":
            root = ET.fromstring(text)
            return _convert_xml_to_dict(root)
    except Exception as exc:
        # Catch any exception from the parser and wrap it
        raise ValueError(f"Failed to deserialize data as {allowed_format}") from exc

# Example usage:
if __name__ == "__main__":
    # JSON example
    json_bytes = b'{"name": "Alice", "age": 30}'
    print(safe_deserialize(json_bytes, "json"))

    # XML example
    xml_bytes = b'<person><name>Alice</name><age>30</age></person>'
    print(safe_deserialize(xml_bytes, "xml"))