import json
import xml.etree.ElementTree as ET
from typing import Any

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Safely deserialize data from a trusted subset of formats.

    Parameters
    ----------
    encoded_data : bytes
        Serialized data in byte form.
    method : str
        Serialization format used. Supported values are:
            - 'json'
            - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise ValueError("encoded_data must be bytes or bytearray")

    method = method.lower()
    if method == "json":
        try:
            return json.loads(encoded_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == "xml":
        try:
            # ElementTree is safe for basic XML parsing and does not
            # automatically resolve external entities.
            return ET.fromstring(encoded_data.decode("utf-8"))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Disallow pickle, yaml, marshal, and any other potentially dangerous formats
        raise ValueError(f"Unsupported or unsafe deserialization method: {method}")