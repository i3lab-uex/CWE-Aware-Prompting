import json
import xml.etree.ElementTree as ET
from typing import Any

# A small set of safe, non-executable serialization formats.
ALLOWED_FORMATS = {
    "json",
    "xml",
}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes data from a restricted set of formats.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    serialization_format : str
        One of the allowed format identifiers ('json', 'xml').

    Returns
    -------
    Any
        The Python object representation of the data.

    Raises
    ------
    ValueError
        If an unsupported format is requested or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    try:
        if fmt == "json":
            # Decode bytes to string using UTF-8 (common for JSON).
            text = raw_data.decode("utf-8")
            return json.loads(text)

        if fmt == "xml":
            # Parse XML from bytes. ElementTree.parse expects a file-like object, so we use BytesIO.
            # No external entities or DTD processing to avoid XXE attacks.
            return ET.fromstring(raw_data)

    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc
    except ET.ParseError as exc:
        raise ValueError(f"Failed to deserialize XML data: {exc}") from exc

    # The control flow should never reach this point because all allowed formats are handled above.
    raise ValueError("Unexpected error during deserialization")