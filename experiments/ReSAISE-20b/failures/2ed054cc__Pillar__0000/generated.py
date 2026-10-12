import json
import xml.etree.ElementTree as ET

# Define the list of safe, supported serialization formats.
SAFE_FORMATS = {"json", "xml"}

def deserialize_data(raw_data: bytes, serialization_format: str):
    """
    Safely deserializes `raw_data` according to the specified `serialization_format`.

    Parameters
    ----------
    raw_data : bytes
        The serialized data to be deserialized.
    serialization_format : str
        One of the supported formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    try:
        if fmt == "json":
            # JSON expects a text string; decode using UTF-8.
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "xml":
            # Parse XML into an ElementTree element.
            return ET.fromstring(raw_data)
    except Exception as exc:
        # Wrap any exception to avoid leaking low‑level details.
        raise ValueError(f"Deserialization error for format '{serialization_format}': {exc}") from exc