import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Deserialize `input_data` based on the specified `serialization_format`.

    Supported formats:
        - 'json': Safely parses JSON into Python objects.
        - 'xml' : Parses XML into an ElementTree.Element.

    Any other format raises ValueError. The function avoids unsafe
    deserialization mechanisms such as pickle.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    serialization_format : str
        The name of the serialization format used.

    Returns
    -------
    object
        The deserialized Python object (dict, list, etc. for JSON; ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be of type 'bytes'")

    fmt = serialization_format.lower()
    if fmt == "json":
        try:
            # JSON expects a text string; decode using UTF-8
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif fmt == "xml":
        try:
            # Parse XML safely; ElementTree does not evaluate external entities
            return ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    else:
        # Disallow any other format (e.g., pickle, marshal, etc.)
        raise ValueError(f"Unsupported or dangerous serialization format: '{serialization_format}'")