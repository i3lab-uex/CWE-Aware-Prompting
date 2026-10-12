import json
import xml.etree.ElementTree as ET
from typing import Any, Dict


def _xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text content is stored under the key '#text'. Child elements are
    converted into nested dictionaries. If multiple children share
    the same tag, they are stored in a list.
    """
    node: Dict[str, Any] = {}
    if element.attrib:
        node.update({f"@{k}": v for k, v in element.attrib.items()})
    if element.text and element.text.strip():
        node["#text"] = element.text.strip()

    children: Dict[str, Any] = {}
    for child in element:
        child_dict = _xml_to_dict(child)
        tag = child.tag
        if tag in children:
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    node.update(children)
    return node


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize `input_data` from the specified `data_type`.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte form.
    data_type : str
        Serialization format. Allowed values are:
            - 'json'
            - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_type` is unsupported or dangerous (e.g., 'pickle').
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be of type 'bytes'")

    data_type = data_type.lower()

    if data_type == "json":
        try:
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if data_type == "xml":
        try:
            root = ET.fromstring(input_data)
            return {root.tag: _xml_to_dict(root)}
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow dangerous or unsupported formats
    raise ValueError(f"Unsupported data type: {data_type}")