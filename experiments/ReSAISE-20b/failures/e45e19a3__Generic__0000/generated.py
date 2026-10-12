import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Safely deserialize `input_data` based on the specified `data_type`.

    Supported formats:
        - 'json': deserializes JSON into Python objects.
        - 'xml' : parses XML and returns an ElementTree.Element.

    Raises:
        ValueError: If `data_type` is not supported or the data cannot be parsed.
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be of type 'bytes'")

    data_type = data_type.lower()

    if data_type == "json":
        try:
            text = input_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if data_type == "xml":
        try:
            text = input_data.decode("utf-8")
            return ET.fromstring(text)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow potentially unsafe formats (e.g., pickle, yaml, etc.)
    raise ValueError(f"Unsupported or dangerous data_type: {data_type}")