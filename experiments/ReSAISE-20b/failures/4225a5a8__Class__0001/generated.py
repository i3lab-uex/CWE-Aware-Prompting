import json
import xml.etree.ElementTree as ET
from typing import Any

def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize raw data from a trusted source.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of the object.
    method_name : str
        One of 'json', 'xml'.  Other values are considered unsafe.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method_name is unsupported or dangerous, or if deserialization fails.
    """
    if not isinstance(raw_data, (bytes, bytearray)):
        raise ValueError("raw_data must be bytes-like")

    method = method_name.lower()

    if method == "json":
        try:
            # Decode bytes to str and parse JSON
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            # Parse XML into an ElementTree.Element
            return ET.fromstring(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow pickle and other potentially dangerous formats
    raise ValueError(f"Unsupported or unsafe deserialization method: {method_name}")