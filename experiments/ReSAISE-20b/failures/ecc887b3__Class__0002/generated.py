import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the list of formats that are considered safe.
SAFE_FORMATS = {
    "json",
    "xml",
}

def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data from raw bytes.
    """
    # Decode to string using UTF-8.  Raise UnicodeDecodeError if invalid.
    text = data.decode("utf-8")
    return json.loads(text)

def _deserialize_xml(data: bytes) -> Any:
    """
    Deserialize XML data from raw bytes.
    Returns the root Element.  The caller can navigate this tree safely.
    """
    # Parse XML without DTD or external entity resolution to avoid XXE attacks.
    parser = ET.XMLParser(resolve_entities=False)
    return ET.fromstring(data, parser=parser)

# Mapping from format name to deserialization function.
_DESERIALIZERS = {
    "json": _deserialize_json,
    "xml": _deserialize_xml,
}

def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize `serialized_bytes` according to the specified
    `allowed_format`.  Only formats listed in SAFE_FORMATS are permitted.
    
    Parameters:
        serialized_bytes (bytes): The raw bytes to deserialize.
        allowed_format (str): One of the supported format names
            ('json', 'xml').

    Returns:
        Any: The Python object resulting from deserialization.

    Raises:
        ValueError: If `allowed_format` is not in SAFE_FORMATS.
        json.JSONDecodeError / ET.ParseError: If the data is malformed
            for the chosen format.
    """
    fmt = allowed_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    deserializer = _DESERIALIZERS[fmt]
    return deserializer(serialized_bytes)