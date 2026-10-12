import json
from typing import Any

# Use a safe XML parser to avoid XXE attacks
try:
    # defusedxml is a safer alternative to the standard library's ElementTree
    from defusedxml import ElementTree as ET
except ImportError:
    # Fallback to the standard library if defusedxml is not available.
    # Note: this fallback should be used with caution as it may expose XXE vulnerabilities.
    import xml.etree.ElementTree as ET


def _parse_json(data: bytes) -> Any:
    """Deserialize JSON data from bytes."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data must be UTF-8 encoded") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _parse_xml(data: bytes) -> Any:
    """Deserialize XML data from bytes into an ElementTree.Element."""
    try:
        element = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data") from exc
    return element


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize raw byte data into Python objects from trusted formats.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte format.
    data_type : str
        Serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data_type is unsupported or deserialization fails.
    """
    if not isinstance(input_data, bytes):
        raise ValueError("input_data must be of type 'bytes'")

    data_type = data_type.lower()
    if data_type == "json":
        return _parse_json(input_data)
    elif data_type == "xml":
        return _parse_xml(input_data)
    else:
        raise ValueError(
            f"Unsupported data type '{data_type}'. "
            "Only 'json' and 'xml' are allowed for security reasons."
        )