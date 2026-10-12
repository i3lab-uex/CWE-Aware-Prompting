import json
import xml.etree.ElementTree as ET

# List of allowed serialization formats.
ALLOWED_FORMATS = {"json", "xml"}

def deserialize_data(raw_data: bytes, serialization_format: str):
    """
    Safely deserialize raw bytes into a Python object based on the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    serialization_format : str
        One of the supported formats ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python data structure.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {serialization_format!r}")

    try:
        if fmt == "json":
            # Decode bytes to str and load JSON safely.
            text = raw_data.decode("utf-8")
            return json.loads(text)

        if fmt == "xml":
            # Parse XML safely; ElementTree does not execute code.
            return ET.fromstring(raw_data)

    except Exception as exc:
        # Wrap any parsing exception in a ValueError for consistency.
        raise ValueError(f"Failed to deserialize data as {serialization_format!r}: {exc}") from exc