import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

# Allowed formats for safe deserialization
ALLOWED_FORMATS = {"json", "xml"}

def _etree_to_dict(elem: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an ElementTree element into a dictionary.
    Attributes are prefixed with '@', text content is stored under '#text'.
    Child elements are added as nested dictionaries or lists if repeated.
    """
    d: Dict[str, Any] = {}
    # Process attributes
    for k, v in elem.attrib.items():
        d[f"@{k}"] = v

    # Process child elements
    children: Dict[str, Any] = {}
    for child in elem:
        child_dict = _etree_to_dict(child)
        tag = child.tag
        if tag in children:
            # Existing tag: convert to list or append
            if not isinstance(children[tag], list):
                children[tag] = [children[tag]]
            children[tag].append(child_dict)
        else:
            children[tag] = child_dict

    d.update(children)

    # Process text
    text = elem.text.strip() if elem.text else ""
    if text:
        d["#text"] = text

    return d


def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        The serialized representation of the data.
    data_format : str
        One of 'json' or 'xml'.  Other formats are rejected.

    Returns
    -------
    Any
        The deserialized Python object.  For JSON it is the result of json.loads.
        For XML it is a nested dictionary representation.

    Raises
    ------
    ValueError
        If `data_format` is not in the allowed list.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    try:
        text = bytes_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8") from exc

    if fmt == "json":
        # json.loads already protects against code execution
        return json.loads(text)

    if fmt == "xml":
        # Parse XML safely; ElementTree does not execute code
        root = ET.fromstring(text)
        return {root.tag: _etree_to_dict(root)}

    # This point is unreachable because of the earlier check
    raise ValueError(f"Unhandled format: {data_format!r}")