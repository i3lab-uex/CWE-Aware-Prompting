import json
import xml.etree.ElementTree as ET

# Allowed formats for safe deserialization
ALLOWED_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        One of the allowed formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format}")

    # Decode bytes to text for JSON and XML
    try:
        text = bytes_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        try:
            return ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {data_format}")