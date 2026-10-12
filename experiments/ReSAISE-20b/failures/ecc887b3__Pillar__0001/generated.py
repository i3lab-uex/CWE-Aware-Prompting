import json
import xml.etree.ElementTree as ET
from typing import Any


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize a byte string into a Python object using only approved formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte representation of the serialized data.
    allowed_format : str
        One of the supported serialization formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object. For JSON, this will be a dict/list/primitive.
        For XML, an ``xml.etree.ElementTree.Element`` instance is returned.

    Raises
    ------
    ValueError
        If the requested format is not supported or if deserialization fails.
    """
    # Normalise the format name
    fmt = allowed_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to str assuming UTF-8; raise if invalid
            text = serialized_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 encoded JSON data: {exc}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON decoding error: {exc}") from exc

    elif fmt == "xml":
        try:
            # Parse XML directly from bytes (ElementTree accepts bytes)
            return ET.fromstring(serialized_bytes)
        except ET.ParseError as exc:
            raise ValueError(f"XML parsing error: {exc}") from exc

    else:
        # Unsupported format
        raise ValueError(f"Unsupported or unsafe serialization format: {allowed_format}")