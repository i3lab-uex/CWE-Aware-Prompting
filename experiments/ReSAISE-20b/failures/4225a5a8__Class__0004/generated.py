import json
import xml.etree.ElementTree as ET
from io import BytesIO

def _xml_to_dict(elem):
    """Recursively convert an ElementTree element into a dictionary."""
    d = {}
    # include attributes
    if elem.attrib:
        d.update({f"@{k}": v for k, v in elem.attrib.items()})
    # include text
    if elem.text and elem.text.strip():
        d["#text"] = elem.text.strip()
    # include children
    for child in elem:
        child_dict = _xml_to_dict(child)
        tag = child.tag
        if tag in d:
            # already exists, convert to list
            if not isinstance(d[tag], list):
                d[tag] = [d[tag]]
            d[tag].append(child_dict)
        else:
            d[tag] = child_dict
    return d

def objectify_data(raw_data: bytes, method_name: str):
    """
    Deserialize `raw_data` into a Python object according to the specified
    `method_name`. Only 'json' and 'xml' are supported. Any other format,
    especially pickle, raises ValueError.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    method_name : str
        One of 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially unsafe.
    """
    method = method_name.lower()
    if method == 'json':
        try:
            # Decode bytes to string using UTF-8; errors='strict' will raise
            text = raw_data.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == 'xml':
        try:
            # Parse XML safely without external libraries
            tree = ET.parse(BytesIO(raw_data))
            root = tree.getroot()
            return {root.tag: _xml_to_dict(root)}
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Any other method is considered unsafe or unsupported
    raise ValueError(f"Unsupported or dangerous format: {method_name}")