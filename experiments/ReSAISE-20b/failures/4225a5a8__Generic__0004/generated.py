import json
import xml.etree.ElementTree as ET
from typing import Any


def _xml_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text nodes are stripped; attributes are prefixed with '@'.
    """
    node: dict = {}
    if element.attrib:
        for k, v in element.attrib.items():
            node[f"@{k}"] = v

    children = list(element)
    if children:
        child_dict: dict[str, Any] = {}
        for child in children:
            child_obj = _xml_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # Multiple children with the same tag become a list
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_obj)
            else:
                child_dict[tag] = child_obj
        node.update(child_dict)

    text = element.text.strip() if element.text else ""
    if text and not children:
        node["#text"] = text

    return node


def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize *raw_data* according to *method_name*.

    Supported formats are:
        - 'json': JSON data (safe).
        - 'xml' : XML data, converted to a dictionary.
    Pickle and other formats are explicitly disallowed.

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte form.
    method_name : str
        The serialization format used ('json', 'xml', etc.).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially dangerous.
    """
    if not isinstance(raw_data, (bytes, bytearray)):
        raise TypeError("raw_data must be bytes-like")

    fmt = method_name.lower()
    if fmt == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(raw_data.decode("utf-8"))
            return {root.tag: _xml_to_dict(root)}
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Pickle and other formats are considered dangerous
    if fmt == "pickle":
        raise ValueError("Deserialization of pickle data is not permitted due to security risks")

    # Any other format is unsupported
    raise ValueError(f"Unsupported deserialization method: {method_name}")