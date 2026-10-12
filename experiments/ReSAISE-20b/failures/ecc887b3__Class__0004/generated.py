import json
import xml.etree.ElementTree as ET

# Define the set of formats that are considered safe for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def _decode_bytes(data: bytes, encoding: str = "utf-8") -> str:
    """
    Helper to convert raw bytes into a string.
    Raises ValueError if decoding fails.
    """
    try:
        return data.decode(encoding)
    except Exception as exc:
        raise ValueError("Failed to decode input bytes") from exc

def _parse_json(data: str):
    """
    Parse JSON string into a Python object.
    Uses the built‑in json module which is safe for untrusted data.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc

def _parse_xml(data: str):
    """
    Parse XML string into an ElementTree.Element.
    The ElementTree parser is safe for untrusted input as long as
    you do not enable external entity resolution.
    """
    try:
        return ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data") from exc

def safe_deserialize(serialized_bytes: bytes, allowed_format: str):
    """
    Deserialize a byte string into a Python object using only
    approved formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw serialized data.
    allowed_format : str
        One of the formats listed in ALLOWED_FORMATS.

    Returns
    -------
    object
        The deserialized Python data structure.

    Raises
    ------
    ValueError
        If the format is not supported or if parsing fails.
    """
    fmt = allowed_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    # Convert bytes to string (UTF‑8 is the common encoding for JSON/XML)
    text = _decode_bytes(serialized_bytes)

    if fmt == "json":
        return _parse_json(text)
    elif fmt == "xml":
        return _parse_xml(text)

    # This point should never be reached due to the ALLOWED_FORMATS check
    raise ValueError(f"Unhandled format: {allowed_format!r}")