import json
import xml.etree.ElementTree as ET

# Whitelist of safe serialization formats
ALLOWED_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize data from a known safe format.

    Parameters
    ----------
    bytes_data : bytes
        Raw serialized data.
    data_format : str
        The format used for serialization ('json' or 'xml').

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a native Python data structure.
        For XML, an ElementTree.Element representing the root node.

    Raises
    ------
    ValueError
        If the requested format is not in the allowed list.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format}")

    if fmt == "json":
        # Decode bytes to string using UTF-8 (common for JSON)
        try:
            text = bytes_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF‑8 encoded") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        # Parse XML safely with ElementTree
        try:
            root = ET.fromstring(bytes_data)
            return root
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # This point should never be reached because of the whitelist check
    raise ValueError(f"Unhandled format: {data_format}")