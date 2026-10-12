import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the list of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "xml"}


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes raw byte data into a Python object.

    Parameters
    ----------
    raw_data : bytes
        Serialized representation of the data.
    serialization_format : str
        The format used for serialization. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list, Element).

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    try:
        if fmt == "json":
            # json.loads expects a str, so decode using UTF-8.
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "xml":
            # ElementTree parses bytes directly.
            return ET.fromstring(raw_data)
    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc