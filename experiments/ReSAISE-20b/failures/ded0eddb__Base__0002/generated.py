import json
import xml.etree.ElementTree as ET
from typing import Any

__all__ = ["load_serialized_data"]

# Safe list of supported formats
SAFE_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize *bytes_data* according to the specified *data_format*.

    Parameters
    ----------
    bytes_data : bytes
        Raw serialized data received from an external source.
    data_format : str
        The format of the serialization. Supported values are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object. For JSON the result will be a native
        Python data structure (dict, list, etc.). For XML it returns an
        ``xml.etree.ElementTree.Element`` instance representing the root node.

    Raises
    ------
    ValueError
        If *data_format* is not one of the supported safe formats.
    """
    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    # Decode the bytes to a string using UTF-8.  Any decoding errors will
    # raise a UnicodeDecodeError, which propagates to the caller.
    text = bytes_data.decode("utf-8")

    if fmt == "json":
        # json.loads safely parses JSON into Python primitives.
        return json.loads(text)

    if fmt == "xml":
        # ElementTree parses XML into an element tree.  It does not
        # execute arbitrary code, so it is considered safe for trusted
        # XML schemas.  The caller can further validate the structure if
        # required.
        return ET.fromstring(text)

    # This point is unreachable due to the earlier check, but keeps
    # type-checkers happy.
    raise ValueError(f"Unhandled format: {data_format!r}")