import json
import xml.etree.ElementTree as ET
from typing import Any

# Predefined safe formats
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize `serialized_data` based on the provided `format_type`.

    Parameters
    ----------
    serialized_data : bytes
        The raw data to deserialize.
    format_type : str
        One of the allowed formats: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_type` is not in the allowed set or if deserialization fails.
    """
    # Ensure only trusted formats are processed
    format_type = format_type.lower()
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    try:
        if format_type == "json":
            # JSON is text-based; decode bytes to string first
            return json.loads(serialized_data.decode("utf-8"))

        if format_type == "xml":
            # XML is parsed into an ElementTree element
            return ET.fromstring(serialized_data)

    except Exception as exc:
        # Wrap any parsing error into a ValueError to keep the API consistent
        raise ValueError(f"Deserialization failed for format '{format_type}': {exc}") from exc