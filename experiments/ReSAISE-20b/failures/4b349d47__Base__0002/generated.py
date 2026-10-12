import json
import xml.etree.ElementTree as ET

# Define the set of trusted formats
TRUSTED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Convert serialized data back into a Python object.
    
    Parameters
    ----------
    serialized_data : bytes
        The serialized object in byte form.
    format_type : str
        One of the permitted serialized data formats ('json', 'xml').
    
    Returns
    -------
    object
        The converted Python object.
    
    Raises
    ------
    ValueError
        If the requested format is not in the set of trusted formats.
    """
    if format_type not in TRUSTED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    # Ensure the data is decoded to a string for JSON and XML parsing
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if format_type == "json":
        # json.loads safely parses JSON into Python primitives
        return json.loads(text)

    if format_type == "xml":
        # ElementTree parses XML; the result is an Element tree
        return ET.fromstring(text)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_type!r}")