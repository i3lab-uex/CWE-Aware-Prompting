import json
import xml.etree.ElementTree as ET

def objectify_data(raw_data: bytes, method_name: str):
    """
    Deserialize `raw_data` according to the specified `method_name`.

    Supported formats:
        - 'json': deserializes JSON data into Python objects.
        - 'xml' : parses XML data and returns the ElementTree root element.

    Any other format raises a ValueError to prevent unsafe or unsupported
    deserialization (e.g., pickle, YAML, etc.).

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte format.
    method_name : str
        The name of the serialization format ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python object (dict/list for JSON, ElementTree.Element
        for XML).

    Raises
    ------
    ValueError
        If the format is unsupported or potentially dangerous.
    """
    if not isinstance(raw_data, bytes):
        raise TypeError("raw_data must be of type 'bytes'")

    fmt = method_name.lower()
    if fmt == "json":
        # JSON is safe for deserialization of basic data structures.
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        # ElementTree parses XML into a tree of Elements.
        try:
            return ET.fromstring(raw_data.decode("utf-8"))
        except (ET.ParseError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Any other format is explicitly disallowed.
    raise ValueError(f"Unsupported or dangerous format: {method_name}")