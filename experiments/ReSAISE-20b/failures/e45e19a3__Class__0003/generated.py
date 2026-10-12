import json
import xml.etree.ElementTree as ET

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "xml"}

def _parse_xml(data: str):
    """
    Parse XML data into an ElementTree.Element.
    Uses a safe parser that does not resolve external entities.
    """
    try:
        # ElementTree's fromstring is safe against XXE by default
        element = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML data: {exc}") from None
    return element

def deserialize_data(input_data: bytes, data_type: str):
    """
    Deserialize `input_data` (bytes) into a Python object according to
    the specified `data_type`.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte format.
    data_type : str
        The serialization format. Supported values are:
            * 'json' - JSON data
            * 'xml'  - XML data

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the `data_type` is not supported or if the data cannot be parsed.
    """
    if not isinstance(input_data, bytes):
        raise ValueError("input_data must be of type 'bytes'")

    data_type = data_type.lower()
    if data_type not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or dangerous format: '{data_type}'")

    # Decode the bytes to a string using UTF-8, which is safe for JSON and XML.
    try:
        data_str = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Data is not valid UTF-8: {exc}") from None

    if data_type == "json":
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from None

    # data_type == "xml"
    return _parse_xml(data_str)