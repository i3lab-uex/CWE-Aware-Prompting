import json
import xml.etree.ElementTree as ET
from typing import Any

# Define the set of safe, supported serialization formats.
ALLOWED_FORMATS = {"json", "xml"}

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize `byte_data` into a Python object using the specified
    serialization format.

    Parameters
    ----------
    byte_data : bytes
        The serialized object in binary form.
    encoding_type : str
        One of the supported serialization formats ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object. For JSON this will be a dict/list/primitive.
        For XML this will be an `xml.etree.ElementTree.Element` instance.

    Raises
    ------
    ValueError
        If `encoding_type` is not in the list of allowed formats.
    """
    fmt = encoding_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {encoding_type!r}")

    try:
        if fmt == "json":
            # JSON strings are UTF‑8 encoded by convention.
            return json.loads(byte_data.decode("utf-8"))
        elif fmt == "xml":
            # ElementTree parses XML safely; no external entity resolution.
            return ET.fromstring(byte_data)
    except (json.JSONDecodeError, ET.ParseError) as exc:
        # Wrap parsing errors in ValueError to keep the API consistent.
        raise ValueError(f"Failed to deserialize data: {exc}") from exc