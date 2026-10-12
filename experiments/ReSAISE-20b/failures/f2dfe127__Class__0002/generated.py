import json
import xml.etree.ElementTree as ET
from typing import Any

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize data from raw bytes into a Python object, allowing only
    a whitelist of safe formats.

    Parameters:
        data_bytes (bytes): The serialized object in byte format.
        format_name (str): The serialization format ('json', 'xml').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or considered unsafe.
        json.JSONDecodeError / ET.ParseError: Propagated from the underlying
            parser for malformed input.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be bytes or bytearray")

    fmt = format_name.lower()
    if fmt == "json":
        # JSON is safe for basic data structures (dict, list, str, int, float, bool, None)
        return json.loads(data_bytes.decode("utf-8"))
    elif fmt == "xml":
        # Parse XML into an ElementTree; users can convert it to a dict if needed.
        return ET.fromstring(data_bytes.decode("utf-8"))
    else:
        # Reject any format that could execute code or be unsafe
        raise ValueError(f"Unsupported or dangerous format: {format_name!r}")