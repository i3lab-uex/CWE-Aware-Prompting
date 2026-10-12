import json
import xml.etree.ElementTree as ET

# Predefined set of allowed formats for data deserialization
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Deserialize the given byte string into a Python object only if the
    format is trusted.

    Parameters:
        serialized_data (bytes): The serialized object in byte form.
        format_type (str): One of the permitted serialized data formats
                           ('json', 'xml').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format_type is not in ALLOWED_FORMATS.
        json.JSONDecodeError / ET.ParseError: If the data cannot be parsed
            according to its format.
    """
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # Convert bytes to string for JSON/XML parsing
    text = serialized_data.decode('utf-8')

    if format_type == "json":
        return json.loads(text)

    # format_type == "xml"
    # For XML we return the ElementTree root element.
    # Consumers can further process this as needed.
    return ET.fromstring(text)