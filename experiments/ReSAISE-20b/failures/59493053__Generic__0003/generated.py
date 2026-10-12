import json
import xml.etree.ElementTree as ET

# Only these formats are allowed for deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Deserialize `input_data` from the specified format into a Python object.
    
    Parameters
    ----------
    input_data : bytes
        Serialized data in byte form.
    serialization_format : str
        The format used for serialization. Must be one of the allowed formats.
    
    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list, ElementTree.Element).
    
    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    TypeError
        If `input_data` is not of type bytes or if the format string is not a string.
    """
    
    # Validate input types
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be of type 'bytes'")
    if not isinstance(serialization_format, str):
        raise TypeError("serialization_format must be a string")
    
    fmt = serialization_format.lower()
    
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or dangerous format: '{serialization_format}'")
    
    try:
        if fmt == "json":
            # Decode bytes to string before parsing
            text = input_data.decode("utf-8")
            return json.loads(text)
        elif fmt == "xml":
            # Parse XML into an ElementTree.Element
            return ET.fromstring(input_data)
    except Exception as exc:
        # Wrap any parsing error into ValueError for consistency
        raise ValueError(f"Failed to deserialize data as {serialization_format}: {exc}") from exc