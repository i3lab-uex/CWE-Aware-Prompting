import json
from xml.etree import ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Safely deserializes raw bytes into Python objects for a limited set of trusted formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte format.
    data_type : str
        The serialization format ('json' or 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or dangerous.
    """
    # Ensure we only accept a limited set of safe formats
    allowed_formats = {"json", "xml"}

    if data_type not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe format: {data_type!r}")

    try:
        # Decode bytes to string for text-based formats
        if data_type == "json":
            text = input_data.decode("utf-8")
            # json.loads already protects against code execution
            return json.loads(text)

        if data_type == "xml":
            # Parse XML into an ElementTree element
            return ET.fromstring(input_data)

    except (UnicodeDecodeError, json.JSONDecodeError, ET.ParseError) as exc:
        # Wrap low-level parsing errors in a ValueError for consistency
        raise ValueError(f"Failed to deserialize {data_type} data: {exc}") from exc