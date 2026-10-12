import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Deserialize `input_data` from a trusted format into a Python object.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        The serialization format. Supported values are:
            - 'json'
            - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_type` is not one of the supported formats.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    # Normalize data type string
    fmt = data_type.strip().lower()

    if fmt == 'json':
        # JSON is safe for deserialization as it only supports basic data types
        return json.loads(input_data.decode('utf-8'))

    elif fmt == 'xml':
        # XML parsing is safe but we do not evaluate any external entities
        parser = ET.XMLParser(resolve_entities=False)
        return ET.fromstring(input_data, parser=parser)

    else:
        # Reject any other format (pickle, marshal, etc.) to avoid security risks
        raise ValueError(f"Unsupported or unsafe data type: {data_type!r}")