import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Safely deserializes data from a supported format.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte form.
    serialization_format : str
        One of 'json', 'xml'. The string is case‑insensitive.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially dangerous.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = serialization_format.strip().lower()

    if fmt == "json":
        try:
            text = input_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            text = input_data.decode("utf-8")
            # ElementTree.fromstring parses XML into an Element.
            # The caller can further process this element if needed.
            return ET.fromstring(text)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow pickle and any other formats for security reasons.
    raise ValueError(f"Unsupported or dangerous format: {serialization_format}")