import json
import xml.etree.ElementTree as ET
from typing import Any, Union


def deserialize_data(input_data: bytes,
                     serialization_format: str) -> Any:
    """
    Safely deserialize data from a restricted set of formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data.
    serialization_format : str
        Format of the serialized data. Allowed values are:
            - 'json'  : JSON format
            - 'xml'   : XML format (parsed into an ElementTree)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # json.loads expects a string; decode with UTF-8
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            # ElementTree parses XML into a tree; no eval or code execution
            return ET.fromstring(input_data.decode("utf-8"))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow any other format
    raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format!r}")