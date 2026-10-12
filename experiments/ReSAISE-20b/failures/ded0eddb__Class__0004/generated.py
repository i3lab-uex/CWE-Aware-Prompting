import json
import xml.etree.ElementTree as ET

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Supported formats:
        - 'json' : JSON text
        - 'xml'  : XML document

    Parameters
    ----------
    bytes_data : bytes
        The serialized representation of a Python object.
    data_format : str
        One of the supported formats ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python data structure.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {'json', 'xml'}

    if data_format not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    try:
        if data_format == 'json':
            # Decode bytes to str using UTF-8 (common for JSON)
            text = bytes_data.decode('utf-8')
            return json.loads(text)

        elif data_format == 'xml':
            # ElementTree parses XML safely; it does not execute code
            return ET.fromstring(bytes_data)

    except Exception as exc:
        # Wrap any exception in ValueError to avoid leaking details
        raise ValueError(f"Failed to deserialize data: {exc}") from None