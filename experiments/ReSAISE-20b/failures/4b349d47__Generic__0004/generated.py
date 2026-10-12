import json
import xml.etree.ElementTree as ET
from typing import Any

# Only these formats are considered safe for deserialization in this context.
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize *serialized_data* according to the specified *format_type*.

    Parameters
    ----------
    serialized_data : bytes
        The raw data to deserialize.
    format_type : str
        One of the permitted formats: 'json', 'xml'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If *format_type* is not in the set of allowed formats.
    """
    format_type = format_type.lower()
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # Convert bytes to a string for JSON/XML parsing
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8") from exc

    if format_type == "json":
        return json.loads(text)

    if format_type == "xml":
        # ElementTree parses XML safely; it does not execute code.
        return ET.fromstring(text)

    # This point should never be reached due to the check above.
    raise ValueError(f"Unhandled format: {format_type}")