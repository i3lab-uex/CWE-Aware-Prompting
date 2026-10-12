import json
import xml.etree.ElementTree as ET
from typing import Any

# Mapping of allowed format names to their corresponding deserialization functions.
_ALLOWED_FORMATS = {
    "json": json.loads,
    # XML is parsed into an ElementTree.Element; callers can decide how to use it.
    "xml": ET.fromstring,
}

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize raw byte data into a Python object using a safe, predefined format.

    Parameters
    ----------
    data_bytes : bytes
        The serialized object in byte form.
    format_name : str
        Name of the serialization format. Only 'json' and 'xml' are allowed.

    Returns
    -------
    Any
        The deserialized Python object (dict for JSON, ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    # Normalise the format name to lower case for comparison
    fmt = format_name.lower()

    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_name!r}")

    # Decode bytes to string; UTF-8 is a common safe choice for JSON/XML
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    # Perform the deserialization
    try:
        return _ALLOWED_FORMATS[fmt](text)
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError(f"Deserialization failed for format {format_name!r}: {exc}") from exc