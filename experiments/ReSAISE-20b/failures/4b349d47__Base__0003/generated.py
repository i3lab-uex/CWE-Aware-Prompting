import json
import xml.etree.ElementTree as ET

# Predefined set of allowed formats for data deserialization
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Deserialize `serialized_data` according to the specified `format_type`.
    
    Parameters
    ----------
    serialized_data : bytes
        The raw serialized data.
    format_type : str
        One of the permitted serialized data formats ('json', 'xml').
    
    Returns
    -------
    Any
        The deserialized Python object (dict/list for JSON, ElementTree.Element for XML).
    
    Raises
    ------
    ValueError
        If `format_type` is not in the set of allowed formats.
    """
    if format_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    # Decode the bytes to a string using UTF-8 (common text encoding)
    try:
        data_str = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded text") from exc

    if format_type.lower() == "json":
        # json.loads is safe for trusted data; it does not execute code
        return json.loads(data_str)

    if format_type.lower() == "xml":
        # ElementTree can parse XML safely; we return the root element
        try:
            return ET.fromstring(data_str)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # This point should never be reached because of the allowed formats check
    raise ValueError(f"Unhandled format: {format_type!r}")