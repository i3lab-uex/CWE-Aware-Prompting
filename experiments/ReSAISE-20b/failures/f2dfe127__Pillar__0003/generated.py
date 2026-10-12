import json
import xml.etree.ElementTree as ET

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize a byte string into a Python object using only safe formats.

    Supported formats:
        - 'json' : JSON data (decoded as UTF-8)
        - 'xml'  : XML data (parsed into an ElementTree.Element)

    Parameters
    ----------
    data_bytes : bytes
        The raw serialized data.
    format_name : str
        Identifier of the serialization format (case‑insensitive).

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or dangerous.
    """
    if not isinstance(data_bytes, bytes):
        raise TypeError("data_bytes must be of type 'bytes'")

    fmt = format_name.strip().lower()
    if fmt == "json":
        try:
            return json.loads(data_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "xml":
        try:
            return ET.fromstring(data_bytes)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Disallow all other formats (e.g., pickle, yaml, marshal)
    raise ValueError(f"Unsupported or unsafe format: '{format_name}'")