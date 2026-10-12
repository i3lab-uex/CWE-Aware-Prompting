import json
import xml.etree.ElementTree as ET

# Define the set of formats that are allowed for safe deserialization
ALLOWED_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize a byte string into a Python object.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        The format of the serialization. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    object
        The deserialized Python data structure.

    Raises
    ------
    ValueError
        If the format is not supported or unsafe.
    """
    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    if not isinstance(bytes_data, (bytes, bytearray)):
        raise TypeError("bytes_data must be of type bytes or bytearray")

    if data_format == "json":
        # json.loads expects a str; decode using UTF-8
        text = bytes_data.decode("utf-8")
        return json.loads(text)

    if data_format == "xml":
        # Parse XML into an ElementTree element
        return ET.fromstring(bytes_data)

    # This point should never be reached because of the format check above
    raise ValueError(f"Unhandled format: {data_format!r}")