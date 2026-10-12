import json
import xml.etree.ElementTree as ET
from typing import Any

def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize a byte string into a Python object in a secure manner.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    method_name : str
        The serialization format used. Supported values are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method_name is not supported or if deserialization fails.
    """
    # Ensure method name comparison is case-insensitive
    fmt = method_name.lower()

    if fmt == "json":
        try:
            # Decode bytes safely (utf-8) and load JSON
            text = raw_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            # Parse XML into an ElementTree element
            return ET.fromstring(raw_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow pickle or any other format
    raise ValueError(f"Unsupported serialization format: {method_name}")