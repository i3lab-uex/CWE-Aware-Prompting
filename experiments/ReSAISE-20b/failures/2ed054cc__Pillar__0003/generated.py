import json
import xml.etree.ElementTree as ET
from typing import Any

# Whitelist of safe serialization formats
SAFE_FORMATS = {"json", "xml"}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes `raw_data` according to the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    serialization_format : str
        One of the allowed formats ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object (dict/list for JSON,
        ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {serialization_format}")

    try:
        if fmt == "json":
            # Decode bytes to string using UTF-8; errors='strict' ensures invalid data raises
            text = raw_data.decode("utf-8", errors="strict")
            return json.loads(text)

        elif fmt == "xml":
            # Parse XML from bytes directly
            return ET.fromstring(raw_data)

    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        # Wrap underlying errors in a ValueError to keep API consistent
        raise ValueError(f"Deserialization failed for format '{serialization_format}': {exc}") from exc