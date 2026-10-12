import json
import xml.etree.ElementTree as ET

# Define the set of trusted formats that are allowed to be deserialized
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Deserialize `serialized_data` based on the specified `format_type`.

    Parameters
    ----------
    serialized_data : bytes
        The serialized object in byte form.
    format_type : str
        One of the permitted serialized data formats ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python object (dict/list for JSON, ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If `format_type` is not in the set of allowed formats.
    """
    if format_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # Decode the bytes to a string using UTF-8 (safe for both JSON and XML)
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if format_type.lower() == "json":
        # json.loads already provides safe deserialization for JSON
        return json.loads(text)

    if format_type.lower() == "xml":
        # Parse XML into an ElementTree.Element. Users can convert it to a dict if needed.
        return ET.fromstring(text)

    # This point should never be reached because of the earlier check
    raise ValueError(f"Unhandled format: {format_type}")