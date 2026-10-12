import json
import xml.etree.ElementTree as ET
from typing import Any

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize raw bytes into a Python object from a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        Serialized data in byte form.
    format_name : str
        Serialization format to use. Supported formats are:
            - 'json'  : JSON format (via json.loads)
            - 'xml'   : XML format (via xml.etree.ElementTree.fromstring)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    if not isinstance(data_bytes, bytes):
        raise TypeError("data_bytes must be of type 'bytes'")

    fmt = format_name.lower()

    if fmt == "json":
        try:
            return json.loads(data_bytes.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            return ET.fromstring(data_bytes.decode('utf-8'))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow potentially unsafe formats like pickle, marshal, etc.
    raise ValueError(f"Unsupported or unsafe format: {format_name}")