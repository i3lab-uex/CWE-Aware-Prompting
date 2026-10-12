import json
import xml.etree.ElementTree as ET
from typing import Any

# Predefined set of allowed formats for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize the given byte sequence into a Python object using only
    trusted formats.

    Parameters
    ----------
    serialized_data : bytes
        The serialized representation of the object.
    format_type : str
        One of the permitted data formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS.
    """
    if format_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    if format_type.lower() == "json":
        # JSON is safe to load from untrusted data
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if format_type.lower() == "xml":
        # ElementTree can parse XML safely; it does not execute code
        try:
            text = serialized_data.decode("utf-8")
            return ET.fromstring(text)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Should never reach here because of the ALLOWED_FORMATS check
    raise ValueError(f"Unhandled format: {format_type}")