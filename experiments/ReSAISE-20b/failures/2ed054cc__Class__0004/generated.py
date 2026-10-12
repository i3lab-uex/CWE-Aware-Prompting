import json
import xml.etree.ElementTree as ET
from typing import Any

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes raw data into a Python object.

    Parameters
    ----------
    raw_data : bytes
        Serialized representation of the data.
    serialization_format : str
        Format used for serialization. Supported formats are:
            * 'json'  - JSON encoded data
            * 'xml'   - XML encoded data

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    # Normalise the format string
    fmt = serialization_format.strip().lower()

    if fmt == 'json':
        try:
            return json.loads(raw_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == 'xml':
        try:
            # ElementTree parses XML into an element tree
            return ET.fromstring(raw_data.decode('utf-8'))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Reject all other formats to avoid unsafe deserialization
    raise ValueError(f"Unsupported serialization format: '{serialization_format}'. "
                     "Only 'json' and 'xml' are allowed.")