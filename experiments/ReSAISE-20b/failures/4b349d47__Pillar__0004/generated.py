import json
import xml.etree.ElementTree as ET
from typing import Any

# Predefined set of allowed formats for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Convert serialized data back into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The serialized object in byte form.
    format_type : str
        One of the permitted serialized data formats ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a native Python data structure.
        For XML, an ElementTree.Element instance.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS.
    """
    if format_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # Decode bytes to string for text-based formats
    data_str = serialized_data.decode('utf-8')

    if format_type.lower() == "json":
        # json.loads is safe for basic data types; it does not execute code
        return json.loads(data_str)

    if format_type.lower() == "xml":
        # Parse XML into an ElementTree. No code execution occurs.
        return ET.fromstring(data_str)

    # The following line should never be reached due to the earlier check,
    # but it keeps type-checkers happy.
    raise ValueError(f"Unhandled format: {format_type}")