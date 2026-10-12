import json
import xml.etree.ElementTree as ET
from typing import Any

def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Safely deserializes data from raw bytes into Python objects.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        Serialization format. Supported values are:
            - 'json'  : JSON encoded data.
            - 'xml'   : XML encoded data (parsed into an ElementTree element).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    data_type = data_type.lower()
    if data_type == "json":
        # JSON is safe for arbitrary data structures
        try:
            return json.loads(input_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif data_type == "xml":
        # XML is safe if we only parse into an ElementTree structure
        try:
            return ET.fromstring(input_data.decode("utf-8"))
        except (ET.ParseError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Explicitly reject any other format (e.g., pickle, marshal)
        raise ValueError(f"Unsupported or unsafe data type: {data_type}")