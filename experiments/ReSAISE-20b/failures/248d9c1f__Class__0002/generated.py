import json
import xml.etree.ElementTree as ET

def _xml_to_dict(element):
    """
    Recursively convert an XML element into a dictionary.
    Attributes are prefixed with '@', text content is stored under '#text'.
    """
    node = {}
    # Process attributes
    if element.attrib:
        for key, value in element.attrib.items():
            node[f"@{key}"] = value

    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_obj = _xml_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # Ensure we store a list of repeated tags
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_obj)
            else:
                child_dict[tag] = child_obj
        node.update(child_dict)

    # Process text content
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text

    return node


def data_to_object(byte_data: bytes, encoding_type: str):
    """
    Deserialize raw byte data into a Python object using only safe formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data in byte format.
    encoding_type : str
        Serialization format. Supported values are 'json' and 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the encoding_type is unsupported or unsafe.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    encoding_type = encoding_type.lower()
    if encoding_type == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if encoding_type == "xml":
        try:
            text = byte_data.decode("utf-8")
            root = ET.fromstring(text)
            return {root.tag: _xml_to_dict(root)}
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Disallow unsafe formats such as pickle, yaml, etc.
    raise ValueError(f"Unsupported or unsafe encoding_type: '{encoding_type}'")