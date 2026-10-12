import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Safely deserialize `input_data` according to the specified `data_type`.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        Serialization format. Supported values are:
            * 'json' – JSON encoded data.
            * 'xml'  – XML formatted data.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the `data_type` is not supported or if deserialization fails.
    """
    # Normalize data type to lowercase
    fmt = data_type.lower()

    if fmt == 'json':
        try:
            # JSON expects text, decode with UTF‑8
            return json.loads(input_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc

    if fmt == 'xml':
        try:
            # ElementTree parses XML safely; no external entity resolution is performed
            return ET.fromstring(input_data.decode('utf-8'))
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Failed to deserialize XML data: {exc}") from exc

    # Any other format is explicitly disallowed
    raise ValueError(f"Unsupported or unsafe data type: {data_type!r}")