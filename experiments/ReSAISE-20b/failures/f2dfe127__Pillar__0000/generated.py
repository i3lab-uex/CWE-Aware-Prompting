import json
import xml.etree.ElementTree as ET

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize data from raw bytes into a Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized representation of an object.
    format_name : str
        The serialization format. Supported formats are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    # Normalize the format name to lower case
    fmt = format_name.strip().lower()

    if fmt == 'json':
        # JSON is safe for basic data types
        try:
            return json.loads(data_bytes.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == 'xml':
        # XML parsing is safe as long as we do not allow external entities
        try:
            # Parse from string; ElementTree does not resolve external entities by default
            return ET.fromstring(data_bytes.decode('utf-8'))
        except (ET.ParseError, UnicodeDecodeError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or dangerous serialization format: {format_name}")