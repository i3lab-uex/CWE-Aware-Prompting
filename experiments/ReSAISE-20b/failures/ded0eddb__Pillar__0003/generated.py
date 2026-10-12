import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the list of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "xml"}


def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize a byte sequence into a Python object based on the given format.

    Parameters
    ----------
    bytes_data : bytes
        The serialized data as a byte string.
    data_format : str
        Identifier of the serialization format. Supported values are:
            - 'json'  : JSON text
            - 'xml'   : XML document

    Returns
    -------
    Any
        The deserialized Python object. For JSON this is the standard Python data
        structures (dict, list, str, int, etc.). For XML this is an ElementTree
        Element instance representing the root of the parsed XML tree.

    Raises
    ------
    ValueError
        If *data_format* is not in :data:`SAFE_FORMATS` or if the data cannot be
        parsed correctly.
    """
    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    # Decode the bytes to a string using UTF-8.  Errors are ignored to avoid
    # raising unexpected exceptions on malformed input.
    try:
        text = bytes_data.decode("utf-8", errors="ignore")
    except Exception as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON decoding error: {exc}") from exc

    if fmt == "xml":
        try:
            # ElementTree.fromstring parses the XML string and returns an Element.
            return ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError(f"XML parsing error: {exc}") from exc

    # The code should never reach this point because of the earlier format check.
    raise ValueError(f"Unhandled format: {data_format!r}")