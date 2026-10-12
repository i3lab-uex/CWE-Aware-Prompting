import json
from xml.etree import ElementTree as ET

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize a byte string into a Python object.

    Parameters
    ----------
    bytes_data : bytes
        The serialized representation of the data.
    data_format : str
        Identifier for the serialization format. Only a whitelisted set of formats are supported.

    Returns
    -------
    Any
        The deserialized Python object. For 'json' this will be a dict/list/etc.
        For 'xml' this will be an xml.etree.ElementTree.Element.

    Raises
    ------
    ValueError
        If the requested format is not in the allowed list or if deserialization fails.
    """
    # Whitelist of safe formats
    _ALLOWED_FORMATS = {"json", "xml"}

    if data_format not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    try:
        if data_format == "json":
            # Decode bytes to string (UTF-8 is the common default for JSON)
            text = bytes_data.decode("utf-8")
            return json.loads(text)

        if data_format == "xml":
            # Parse XML directly from bytes
            return ET.fromstring(bytes_data)

    except Exception as exc:
        # Wrap any low‑level exception in a ValueError to avoid leaking implementation details
        raise ValueError(f"Failed to deserialize data as {data_format}: {exc}") from exc