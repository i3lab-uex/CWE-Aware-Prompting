import json
import xml.etree.ElementTree as ET
from typing import Any

# Only these formats are considered safe for deserialization of untrusted data.
SAFE_FORMATS = {"json", "xml"}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize raw data into a Python object using only a whitelist of safe formats.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of the data.
    serialization_format : str
        One of 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a dict/list/str/etc.
        For XML, an xml.etree.ElementTree.Element instance.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    try:
        if fmt == "json":
            # json.loads expects a string, so decode bytes safely
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "xml":
            # ET.fromstring expects a string; decode bytes safely
            return ET.fromstring(raw_data.decode("utf-8"))
    except Exception as exc:
        # Wrap any exception in ValueError to avoid leaking implementation details
        raise ValueError(f"Failed to deserialize data: {exc}") from exc