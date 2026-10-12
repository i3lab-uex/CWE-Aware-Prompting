import json
import xml.etree.ElementTree as ET
from typing import Any

# Allowed serialization formats – only those that are safe for untrusted data.
_ALLOWED_FORMATS = {"json", "xml"}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes data from a trusted set of formats.

    Parameters
    ----------
    raw_data : bytes
        The serialized data as a byte string.
    serialization_format : str
        One of 'json' or 'xml'.

    Returns
    -------
    Any
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    try:
        if fmt == "json":
            # JSON expects text; decode using UTF-8
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "xml":
            # Parse XML into an ElementTree.Element
            return ET.fromstring(raw_data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ET.ParseError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc