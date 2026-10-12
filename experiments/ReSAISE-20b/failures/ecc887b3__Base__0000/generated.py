import json
import xml.etree.ElementTree as ET
from typing import Any

# Allowed formats for safe deserialization
ALLOWED_FORMATS = {"json", "xml"}

def _element_to_dict(element: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    Child elements are grouped by tag name. If multiple children share
    the same tag, they are stored as a list.
    """
    node: dict = {}
    if element.attrib:
        node["@attributes"] = dict(element.attrib)

    text = (element.text or "").strip()
    if text:
        node["#text"] = text

    children_by_tag: dict[str, list] = {}
    for child in element:
        child_dict = _element_to_dict(child)
        children_by_tag.setdefault(child.tag, []).append(child_dict)

    for tag, items in children_by_tag.items():
        node[tag] = items if len(items) > 1 else items[0]

    return node

def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Deserialize *serialized_bytes* into a Python object, only if
    the format is in :data:`ALLOWED_FORMATS`.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw bytes containing the serialized data.
    allowed_format : str
        The format of the data, e.g. 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    try:
        if fmt == "json":
            # json.loads accepts str, so decode using utf-8
            return json.loads(serialized_bytes.decode("utf-8"))
        elif fmt == "xml":
            root = ET.fromstring(serialized_bytes)
            return {root.tag: _element_to_dict(root)}
    except Exception as exc:
        raise ValueError(f"Deserialization error for format {allowed_format!r}: {exc}") from exc