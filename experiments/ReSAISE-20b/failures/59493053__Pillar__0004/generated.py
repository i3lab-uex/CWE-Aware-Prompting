import json
import xml.etree.ElementTree as ET
from typing import Any


def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize *input_data* according to the specified *serialization_format*.

    Supported formats:
        - 'json' : safe JSON deserialization
        - 'xml'  : XML parsing into an ElementTree.Element

    The function explicitly disallows pickle and other dangerous formats.
    It raises ValueError for unsupported or potentially unsafe formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte form.
    serialization_format : str
        One of 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *serialization_format* is not supported or considered unsafe.
    """
    # Normalise format name
    fmt = serialization_format.strip().lower()

    if fmt == "json":
        # json.loads expects str, so decode bytes safely
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be valid UTF-8") from exc
        return json.loads(text)

    if fmt == "xml":
        # Parse XML directly from bytes
        try:
            return ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError("Malformed XML data") from exc

    # Explicitly disallow pickle and other formats
    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")