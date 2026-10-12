import json
import xml.etree.ElementTree as ET
import pickle

# Predefined set of trusted formats for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Convert serialized data back into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The serialized representation of the data.
    format_type : str
        One of the permitted formats: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not trusted or unsupported.
    """
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    if format_type == "json":
        # json.loads expects a string, so decode bytes first
        return json.loads(serialized_data.decode("utf-8"))

    if format_type == "xml":
        # Parse XML and convert to a nested dictionary
        root = ET.fromstring(serialized_data)
        return _xml_to_dict(root)

    # This point should never be reached because of the allowed set
    raise ValueError(f"Unhandled format: {format_type}")

def _xml_to_dict(element):
    """
    Recursively convert an ElementTree element into a dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    Child elements are nested accordingly.
    """
    node = {}
    # Handle attributes
    if element.attrib:
        node["@attributes"] = dict(element.attrib)

    # Handle child elements
    children = list(element)
    if children:
        for child in children:
            child_dict = _xml_to_dict(child)
            tag = child.tag
            if tag in node:
                # Multiple children with same tag -> list
                if not isinstance(node[tag], list):
                    node[tag] = [node[tag]]
                node[tag].append(child_dict)
            else:
                node[tag] = child_dict
    # Handle text content
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text

    return node