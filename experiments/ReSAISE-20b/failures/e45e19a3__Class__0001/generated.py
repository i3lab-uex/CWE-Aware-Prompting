import json
from defusedxml.ElementTree import fromstring as safe_xml_fromstring

def deserialize_data(input_data: bytes, data_type: str):
    """
    Deserialize raw byte data into a Python object using only trusted formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte format.
    data_type : str
        Serialization format. Supported values are 'json' and 'xml'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided format is unsupported or considered unsafe.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = data_type.lower()

    if fmt == "json":
        # json.loads expects a string; decode bytes safely
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("Invalid UTF-8 data for JSON") from e
        return json.loads(text)

    elif fmt == "xml":
        # Use defusedxml to guard against XML attacks (e.g., XXE)
        try:
            return safe_xml_fromstring(input_data)
        except Exception as e:
            raise ValueError("Failed to parse XML safely") from e

    else:
        # Reject any other formats (pickle, marshal, etc.) to avoid unsafe deserialization
        raise ValueError(f"Unsupported or unsafe data_type: {data_type}")