import json
import xml.etree.ElementTree as ET


def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Safely deserializes data from a known format.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte form.
    serialization_format : str
        One of 'json', 'xml'.  Other formats are considered unsafe.

    Returns
    -------
    Any
        The deserialized Python object.  For JSON this is a native Python
        structure; for XML it returns an ElementTree.Element.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially unsafe.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = serialization_format.lower()
    try:
        if fmt == "json":
            # JSON is safe as long as we don't execute code.
            return json.loads(input_data.decode("utf-8"))
        elif fmt == "xml":
            # ElementTree parses XML safely without executing code.
            return ET.fromstring(input_data)
        else:
            raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")
    except (json.JSONDecodeError, ET.ParseError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc