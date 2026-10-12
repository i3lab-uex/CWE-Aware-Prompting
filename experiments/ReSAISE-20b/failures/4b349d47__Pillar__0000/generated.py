import json
import xml.etree.ElementTree as ET

# Predefined set of allowed formats for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Convert a byte string containing serialized data into the corresponding
    Python object, but only if the format is explicitly trusted.

    Parameters:
        serialized_data (bytes): The raw bytes representing a serialized object.
        format_type (str): One of the permitted formats ('json', 'xml').

    Returns:
        The deserialized Python object (e.g., dict for JSON, ElementTree.Element
        for XML).

    Raises:
        ValueError: If an untrusted or unsupported format_type is supplied.
    """
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # Convert bytes to string if needed
    try:
        data_str = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data must be valid UTF-8 encoded bytes") from exc

    if format_type == "json":
        # JSON is safe to load because it only creates basic data structures
        return json.loads(data_str)

    if format_type == "xml":
        # Parse XML safely. ElementTree parses from a string without
        # executing arbitrary code, but we still need to handle potential
        # resource exhaustion or malformed XML.
        try:
            return ET.fromstring(data_str)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_type}")