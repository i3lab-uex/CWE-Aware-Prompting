import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Deserialize `serialized_data` according to the specified `format_type`.

    Parameters
    ----------
    serialized_data : bytes
        The byte string containing the serialized object.
    format_type : str
        One of the permitted serialization formats ('json', 'xml').

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
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    try:
        if format_type == "json":
            # json.loads expects a string, so decode the bytes
            return json.loads(serialized_data.decode("utf-8"))

        if format_type == "xml":
            # Parse XML into an ElementTree.Element. Users can convert this
            # to a dictionary or other structure as needed.
            return ET.fromstring(serialized_data.decode("utf-8"))

    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        # Wrap the underlying exception in a ValueError to keep the API clean
        raise ValueError(f"Failed to deserialize data: {exc}") from exc

    # The code should never reach this point because all allowed formats are handled
    raise ValueError(f"Unhandled format: {format_type}")