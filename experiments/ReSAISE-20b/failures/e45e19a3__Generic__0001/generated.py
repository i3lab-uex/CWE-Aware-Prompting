import json
import xml.etree.ElementTree as ET
from typing import Any, Union


def _xml_to_dict(elem: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Attributes are prefixed with '@', text content is stored under '#text'.
    """
    d: dict = {}
    if elem.attrib:
        for k, v in elem.attrib.items():
            d[f"@{k}"] = v

    children = list(elem)
    if children:
        child_dict: dict[str, Union[list, Any]] = {}
        for child in children:
            child_obj = _xml_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                if isinstance(child_dict[tag], list):
                    child_dict[tag].append(child_obj)
                else:
                    child_dict[tag] = [child_dict[tag], child_obj]
            else:
                child_dict[tag] = child_obj
        d.update(child_dict)
    text = elem.text.strip() if elem.text else ""
    if text:
        d["#text"] = text
    return d


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        Serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data_type is unsupported or considered unsafe.
    """
    allowed_formats = {"json", "xml"}
    fmt = data_type.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe data type: {data_type}")

    try:
        if fmt == "json":
            text = input_data.decode("utf-8")
            return json.loads(text)
        elif fmt == "xml":
            root = ET.fromstring(input_data.decode("utf-8"))
            return {root.tag: _xml_to_dict(root)}
    except (json.JSONDecodeError, ET.ParseError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc