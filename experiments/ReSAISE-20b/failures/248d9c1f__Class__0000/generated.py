import json
import xml.etree.ElementTree as ET
from typing import Any

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize `byte_data` into a Python object using the specified
    serialization format.

    Parameters:
        byte_data (bytes): The serialized data.
        encoding_type (str): One of the supported formats ('json', 'xml').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or potentially dangerous.
    """
    if not isinstance(byte_data, (bytes, bytearray)):
        raise TypeError("byte_data must be bytes or bytearray")

    fmt = encoding_type.lower()
    if fmt == "json":
        # Decode bytes to str, then parse JSON safely.
        text = byte_data.decode("utf-8")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        # Parse XML into ElementTree, but do not evaluate any embedded
        # scripts or external entities.  The standard library parser is safe
        # by default for well‑formed XML.
        try:
            root = ET.fromstring(byte_data)
            # Convert the ElementTree to a simple dict representation
            def elem_to_dict(elem):
                return {
                    "tag": elem.tag,
                    "attributes": elem.attrib,
                    "text": (elem.text or "").strip(),
                    "children": [elem_to_dict(child) for child in elem]
                }
            return elem_to_dict(root)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Any other format is considered unsafe or unsupported.
    raise ValueError(f"Unsupported serialization format: {encoding_type!r}")