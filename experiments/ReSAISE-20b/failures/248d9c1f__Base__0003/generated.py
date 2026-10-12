import json
import xml.etree.ElementTree as ET

# Define the set of allowed, safe serialization formats.
ALLOWED_FORMATS = {
    "json",
    "xml",
}

def data_to_object(byte_data: bytes, encoding_type: str):
    """
    Deserialize raw byte data into a Python object using only safe formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in binary form.
    encoding_type : str
        One of the supported serialization formats ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python representation.
        For JSON it returns the parsed data (dict/list/etc.).
        For XML it returns an `xml.etree.ElementTree.Element` tree.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS or if parsing fails.
    """
    fmt = encoding_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {encoding_type!r}")

    try:
        if fmt == "json":
            # JSON decoding is safe for standard data types.
            return json.loads(byte_data.decode("utf-8"))
        elif fmt == "xml":
            # Parse XML from bytes; ElementTree is safe for basic parsing.
            return ET.fromstring(byte_data)
    except Exception as exc:
        # Wrap any parsing exception into ValueError for consistency.
        raise ValueError(f"Failed to deserialize data as {encoding_type}: {exc}") from exc