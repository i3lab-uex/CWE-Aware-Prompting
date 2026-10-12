import json
import xml.etree.ElementTree as ET
from typing import Any


def _parse_xml_to_dict(elem: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a nested dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    Child elements are appended as lists or single dicts depending on occurrence.
    """
    result: dict = {}
    # Attributes
    if elem.attrib:
        result["@attributes"] = dict(elem.attrib)

    # Text content
    text = elem.text.strip() if elem.text else ""
    if text:
        result["#text"] = text

    # Children
    children: dict[str, Any] = {}
    for child in elem:
        child_dict = _parse_xml_to_dict(child)
        tag = child.tag
        if tag in children:
            # existing tag -> make list
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    result.update(children)
    return result


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized representation of the object.
    encoding_type : str
        Serialization format. Supported formats are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the encoding_type is not supported or considered unsafe.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    encoding_type = encoding_type.lower()
    if encoding_type == "json":
        # Decode using UTF-8 (common for JSON)
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if encoding_type == "xml":
        try:
            root = ET.fromstring(byte_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc
        return _parse_xml_to_dict(root)

    # Disallow any other formats (e.g., pickle, msgpack, yaml, etc.)
    raise ValueError(f"Unsupported or unsafe encoding_type: '{encoding_type}'")