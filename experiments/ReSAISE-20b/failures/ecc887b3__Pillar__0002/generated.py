import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

__all__ = ["safe_deserialize"]


def _json_to_python(data: str) -> Any:
    """
    Safely convert a JSON string into a Python object.
    """
    return json.loads(data)


def _xml_to_python(element: ET.Element) -> Dict[str, Any]:
    """
    Convert an XML element into a nested dictionary.
    This is a simple and safe conversion that only keeps
    tag names, attributes and text content.
    """
    def _elem_to_dict(elem: ET.Element) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if elem.attrib:
            result.update({f"@{k}": v for k, v in elem.attrib.items()})
        if elem.text and elem.text.strip():
            result["#text"] = elem.text.strip()
        for child in elem:
            child_dict = _elem_to_dict(child)
            tag = child.tag
            if tag in result:
                # If the same tag already exists, convert to list
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_dict)
            else:
                result[tag] = child_dict
        return result

    return {element.tag: _elem_to_dict(element)}


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Deserialize ``serialized_bytes`` into a Python object while
    restricting the operation to a whitelist of safe formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data to be deserialized.
    allowed_format : str
        One of the supported formats: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the allowed list or if deserialization fails.
    """
    if not isinstance(serialized_bytes, (bytes, bytearray)):
        raise ValueError("Input must be bytes or bytearray")

    fmt = allowed_format.lower()
    if fmt == "json":
        try:
            text = serialized_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return _json_to_python(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(serialized_bytes)
        except ET.ParseError as exc:
            raise ValueError("Failed to parse XML") from exc
        return _xml_to_python(root)

    # Any other format is explicitly forbidden
    raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")