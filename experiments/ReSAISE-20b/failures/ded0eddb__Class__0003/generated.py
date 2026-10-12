import json
from xml.etree import ElementTree as ET

# Allowed, secure formats for deserialization
ALLOWED_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        Serialized representation of a Python object.
    data_format : str
        The serialization format used ('json' or 'xml').

    Returns
    -------
    object
        The deserialized Python data structure (dict/list for JSON,
        ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If `data_format` is not in the list of allowed formats.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format}")

    if fmt == "json":
        # json.loads expects a str; decode bytes using UTF-8
        return json.loads(bytes_data.decode("utf-8"))

    if fmt == "xml":
        # ElementTree can parse from a bytes buffer directly
        return ET.fromstring(bytes_data)

    # This point should never be reached due to the check above
    raise ValueError(f"Unhandled data format: {data_format}")