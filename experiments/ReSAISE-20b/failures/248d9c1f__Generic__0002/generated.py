import json
import xml.etree.ElementTree as ET

def data_to_object(byte_data: bytes, encoding_type: str):
    """
    Deserialize `byte_data` into a Python object based on the provided
    `encoding_type`. Only safe, trusted formats are supported.

    Parameters
    ----------
    byte_data : bytes
        Serialized data in binary form.
    encoding_type : str
        The serialization format ('json' or 'xml').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns a native
        Python data structure; for XML it returns an ElementTree.Element.

    Raises
    ------
    ValueError
        If the format is unsupported or deemed unsafe.
    """
    # Normalise encoding type to lowercase
    fmt = encoding_type.strip().lower()

    if fmt == 'json':
        try:
            # Decode bytes to string; assume UTF-8
            text = byte_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == 'xml':
        try:
            # ElementTree's parse methods are safe against XML external entities
            return ET.fromstring(byte_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Any other format is considered unsafe or unsupported
        raise ValueError(f"Unsupported serialization format: {encoding_type!r}")