import json
import xml.etree.ElementTree as ET

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize data from raw bytes into a Python object.
    
    Parameters
    ----------
    data_bytes : bytes
        Serialized data in byte format.
    format_name : str
        Serialization format. Supported values are:
        
        * 'json'   – JSON text, safe for arbitrary data.
        * 'xml'    – XML document, parsed into an ElementTree element.
        
    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list, str, etc.).
    
    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be bytes or bytearray")
    
    fmt = format_name.lower()
    
    if fmt == "json":
        # JSON is safe for arbitrary data structures
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 encoding for JSON data") from exc
        return json.loads(text)
    
    if fmt == "xml":
        # ElementTree parses XML into a tree of elements; no arbitrary code execution
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 encoding for XML data") from exc
        return ET.fromstring(text)
    
    # Disallow pickle, marshal, or any other format that can execute code
    raise ValueError(f"Unsupported or unsafe serialization format: {format_name!r}")