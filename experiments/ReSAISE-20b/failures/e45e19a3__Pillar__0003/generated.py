import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Deserialize raw bytes into a Python object using only trusted formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        Serialization format. Supported values are 'json' and 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = data_type.lower()
    if fmt == 'json':
        try:
            return json.loads(input_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    elif fmt == 'xml':
        try:
            # ElementTree parses XML safely without executing code
            return ET.fromstring(input_data.decode('utf-8'))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Failed to parse XML data") from exc

    else:
        # Reject all other formats, including pickle and unsafe custom serializers
        raise ValueError(f"Unsupported or dangerous data type: {data_type!r}")