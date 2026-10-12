import json
import xml.etree.ElementTree as ET

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize `data_bytes` into a Python object using the specified safe format.

    Parameters
    ----------
    data_bytes : bytes
        The serialized object in byte form.
    format_name : str
        The name of the serialization format. Supported values are:
            - 'json'   : JSON format
            - 'xml'    : XML format (returns an ElementTree.Element)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the allowed list of formats.
    """
    if not isinstance(data_bytes, bytes):
        raise TypeError("data_bytes must be of type 'bytes'")

    # Define the set of trusted formats
    TRUSTED_FORMATS = {"json", "xml"}

    if format_name not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{format_name}'. "
            f"Allowed formats: {', '.join(TRUSTED_FORMATS)}"
        )

    # Decode bytes to string using UTF-8
    text = data_bytes.decode("utf-8")

    if format_name == "json":
        return json.loads(text)

    # XML handling
    if format_name == "xml":
        try:
            # Parse the XML string into an ElementTree.Element
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from None
        return root

    # This point should never be reached because of the earlier check.
    raise ValueError(f"Unhandled format: {format_name}")