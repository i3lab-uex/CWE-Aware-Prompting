import json
import xml.etree.ElementTree as ET
from typing import Any

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize `byte_data` into a Python object using only safe, trusted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data.
    encoding_type : str
        Serialization format. Supported values are:
            - 'json'
            - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `encoding_type` is unsupported or if the data cannot be parsed.
    """
    # Ensure byte_data is a bytes instance
    if not isinstance(byte_data, (bytes, bytearray)):
        raise ValueError("byte_data must be bytes or bytearray")

    # Normalize the format name
    fmt = encoding_type.strip().lower()

    if fmt == 'json':
        try:
            return json.loads(byte_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif fmt == 'xml':
        try:
            # Parse XML into an ElementTree
            root = ET.fromstring(byte_data.decode('utf-8'))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

        # Convert ElementTree to a nested dictionary
        def elem_to_dict(elem: ET.Element) -> Any:
            d = {}
            # Include attributes if any
            if elem.attrib:
                d.update({f"@{k}": v for k, v in elem.attrib.items()})
            # Process child elements
            children = list(elem)
            if children:
                child_dict = {}
                for child in children:
                    child_val = elem_to_dict(child)
                    tag = child.tag
                    if tag in child_dict:
                        # If multiple children with same tag, store as list
                        if not isinstance(child_dict[tag], list):
                            child_dict[tag] = [child_dict[tag]]
                        child_dict[tag].append(child_val)
                    else:
                        child_dict[tag] = child_val
                d.update(child_dict)
            # Include text if present and not just whitespace
            text = elem.text.strip() if elem.text else ''
            if text:
                d['#text'] = text
            return d

        return {root.tag: elem_to_dict(root)}

    else:
        raise ValueError(f"Unsupported or unsafe deserialization format: '{encoding_type}'")