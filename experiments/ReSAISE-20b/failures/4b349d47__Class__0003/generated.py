import json
import xml.etree.ElementTree as ET
from typing import Any

# Define a set of allowed formats for deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize `serialized_data` into a Python object, but only if
    the format is explicitly trusted.

    Parameters:
        serialized_data (bytes): The byte representation of the data.
        format_type (str): One of the permitted serialized data formats
                           ('json', 'xml'). Other values raise ValueError.

    Returns:
        The deserialized Python object (e.g., dict for JSON, ElementTree
        element for XML).

    Raises:
        ValueError: If `format_type` is not in ALLOWED_FORMATS.
        json.JSONDecodeError / ET.ParseError: Propagated from the parser
                                               if data is malformed.
    """
    # Normalise format string to lower case for comparison
    fmt = format_type.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    if fmt == "json":
        # JSON is safe; it only creates basic Python types
        return json.loads(serialized_data.decode("utf-8"))

    if fmt == "xml":
        # XML is safe as long as we don't use any external entities.
        # ElementTree's `fromstring` does not resolve DTDs by default,
        # but we still guard against potential entity expansions.
        parser = ET.XMLParser(resolve_entities=False)
        return ET.fromstring(serialized_data.decode("utf-8"), parser=parser)

    # This point should never be reached because of the guard above.
    raise ValueError(f"Unhandled format: {format_type!r}")