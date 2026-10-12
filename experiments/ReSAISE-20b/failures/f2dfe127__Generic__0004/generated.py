import json
import xml.etree.ElementTree as ET
from typing import Any

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `data_bytes` into a Python object based on the provided format.
    
    Only safe, trusted formats are allowed. Unsupported or potentially dangerous
    formats raise a ValueError.

    Parameters:
        data_bytes (bytes): Serialized object in byte format.
        format_name (str): Serialization format name ('json' or 'xml').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or considered unsafe.
        json.JSONDecodeError / ET.ParseError: Propagated from the underlying parser
            if the data is malformed.
    """
    format_name = format_name.lower()
    if format_name == 'json':
        # Decode bytes to string using UTF-8 and parse JSON
        return json.loads(data_bytes.decode('utf-8'))
    elif format_name == 'xml':
        # Parse XML and return the root Element
        return ET.fromstring(data_bytes)
    else:
        # Explicitly disallow any other formats (e.g., pickle, yaml, etc.)
        raise ValueError(f"Unsupported or unsafe format: {format_name}")