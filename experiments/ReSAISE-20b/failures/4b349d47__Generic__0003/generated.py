import json
import xml.etree.ElementTree as ET
from typing import Any

# Predefined set of allowed formats for data deserialization
ALLOWED_FORMATS = {"json", "xml"}


def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Convert serialized data back into a Python object in a secure manner.

    Parameters
    ----------
    serialized_data : bytes
        The serialized object in byte form.
    format_type : str
        One of the permitted serialized data formats ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object (dict for JSON, ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the format_type is not in the allowed list.
    """
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    if format_type == "json":
        # Decode bytes to string using UTF-8 (common encoding for JSON)
        text = serialized_data.decode("utf-8")
        # json.loads is safe as it only constructs basic Python types
        return json.loads(text)

    if format_type == "xml":
        # Parse XML into an ElementTree.Element.
        # ElementTree is safe for parsing well‑formed XML, but we avoid
        # any external entity resolution to mitigate XXE attacks.
        parser = ET.XMLParser(resolve_entities=False)
        return ET.fromstring(serialized_data, parser=parser)

    # The code should never reach here due to the initial check.
    raise ValueError(f"Unhandled format: {format_type!r}")