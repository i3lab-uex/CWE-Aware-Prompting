import json
import pickle
import xml.etree.ElementTree as ET
from typing import Any

# Allowed formats for deserialization. Pickle is generally unsafe,
# but it can be enabled explicitly by the caller if required.
ALLOWED_FORMATS = {"json", "xml", "pickle"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize `serialized_data` according to the specified `format_type`.

    Parameters
    ----------
    serialized_data : bytes
        The byte sequence containing the serialized object.
    format_type : str
        One of the permitted formats ('json', 'xml', or 'pickle').

    Returns
    -------
    Any
        The deserialized Python object. For XML the function returns an
        ElementTree.Element instance.

    Raises
    ------
    ValueError
        If `format_type` is not in the allowed set.
    """
    # Normalise format string to lowercase for case‑insensitive comparison
    fmt = format_type.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # Convert bytes to string for JSON/XML; pickle works directly on bytes
    if fmt == "json":
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF‑8") from exc
        return json.loads(text)

    if fmt == "xml":
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("XML data is not valid UTF‑8") from exc
        return ET.fromstring(text)

    if fmt == "pickle":
        # Pickle is inherently insecure; only use when explicitly allowed.
        return pickle.loads(serialized_data)

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled format: {format_type}")