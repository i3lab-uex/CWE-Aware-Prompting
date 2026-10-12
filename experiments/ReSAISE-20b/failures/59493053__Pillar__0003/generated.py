import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Deserialize data from a supported format.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte form.
    serialization_format : str
        One of 'json', 'xml'. Any other value raises ValueError.

    Returns
    -------
    object
        The deserialized Python object (dict/list for JSON, ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If an unsupported or dangerous format is requested.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = serialization_format.lower()
    if fmt == 'json':
        try:
            text = input_data.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == 'xml':
        try:
            # ElementTree.parse expects a file-like object; use BytesIO
            from io import BytesIO
            return ET.parse(BytesIO(input_data)).getroot()
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Disallow any other format to prevent unsafe deserialization
    raise ValueError(f"Unsupported serialization format: {serialization_format!r}")