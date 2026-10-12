import json
import xml.etree.ElementTree as ET

# Define a whitelist of safe formats
_ALLOWED_FORMATS = {
    "json": _deserialize_json,
    "xml":  _deserialize_xml
}

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize data from raw bytes into a Python object using a safe, whitelisted format.

    Parameters
    ----------
    data_bytes : bytes
        Serialized object in byte form.
    format_name : str
        Name of the serialization format (e.g., 'json', 'xml').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or deserialization fails.
    """
    # Normalise format name
    fmt = format_name.strip().lower()

    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or dangerous format: '{format_name}'")

    # Delegate to the appropriate deserializer
    try:
        return _ALLOWED_FORMATS[fmt](data_bytes)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Deserialization error for format '{format_name}': {exc}") from exc


def _deserialize_json(data_bytes: bytes):
    """Deserialize JSON data."""
    text = data_bytes.decode("utf-8")
    return json.loads(text)


def _deserialize_xml(data_bytes: bytes):
    """Deserialize XML data into an ElementTree.Element."""
    # Decode bytes to string; ElementTree accepts bytes directly, but
    # decoding allows consistent error handling.
    text = data_bytes.decode("utf-8")
    return ET.fromstring(text)