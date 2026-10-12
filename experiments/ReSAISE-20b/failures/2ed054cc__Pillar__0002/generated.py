import json
import xml.etree.ElementTree as ET
from typing import Any

# Only these formats are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely convert serialized data (bytes) into a Python object.

    Parameters
    ----------
    raw_data : bytes
        Serialized representation of the data.
    serialization_format : str
        The format used for serialization. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_format.lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {serialization_format}")

    try:
        if fmt == "json":
            # Decode bytes to string and load JSON
            text = raw_data.decode("utf-8")
            return json.loads(text)

        if fmt == "xml":
            # Parse XML into an ElementTree element
            return ET.fromstring(raw_data)

    except Exception as exc:
        # Wrap any exception to provide a clear error message
        raise ValueError(f"Failed to deserialize data: {exc}") from exc

    # This point should never be reached due to the format check above
    raise ValueError(f"Unhandled serialization format: {serialization_format}")