import json
import xml.etree.ElementTree as ET

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize `data_bytes` into a Python object using only
    trusted formats.

    Supported formats:
        - 'json': JSON data (safe by default)
        - 'xml' : XML data parsed into an ElementTree.Element

    Parameters
    ----------
    data_bytes : bytes
        Serialized object in byte form.
    format_name : str
        Name of the serialization format ('json' or 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be bytes or bytearray")

    fmt = format_name.lower()
    if fmt == "json":
        try:
            # `json.loads` expects a str; decode with utf-8
            return json.loads(data_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif fmt == "xml":
        try:
            # Parse XML directly from bytes; ElementTree handles it safely
            return ET.fromstring(data_bytes)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    else:
        # Reject any format that could execute code (e.g., pickle, marshal)
        raise ValueError(f"Unsupported or unsafe format: {format_name}")