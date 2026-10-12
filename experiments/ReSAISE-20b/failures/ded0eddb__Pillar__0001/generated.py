import json
import xml.etree.ElementTree as ET

# Allowed formats for deserialization – only those considered safe
ALLOWED_FORMATS = {"json", "xml"}


def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize raw bytes into a Python object.

    Parameters
    ----------
    bytes_data : bytes
        The serialized representation of the data.
    data_format : str
        One of 'json' or 'xml'.  Other values raise ValueError.

    Returns
    -------
    object
        The deserialized Python data structure.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS.
    """
    if data_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{data_format}'. "
            f"Allowed formats: {sorted(ALLOWED_FORMATS)}"
        )

    if data_format.lower() == "json":
        # Decode bytes to str assuming UTF-8; raise if invalid encoding
        try:
            text = bytes_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        # json.loads safely parses JSON into native Python objects
        return json.loads(text)

    if data_format.lower() == "xml":
        # Parse XML from bytes; ElementTree handles the parsing safely
        try:
            return ET.fromstring(bytes_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc