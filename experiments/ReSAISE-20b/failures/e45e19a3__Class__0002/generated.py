import json
import xml.etree.ElementTree as ET
from typing import Any

# A whitelist of safe serialization formats
_TRUSTED_FORMATS = {"json", "xml"}

def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize `input_data` into a Python object according to `data_type`.

    Parameters
    ----------
    input_data : bytes
        The serialized data.
    data_type : str
        Serialization format identifier. Only 'json' and 'xml' are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_type` is not in the trusted set or if parsing fails.
    """
    fmt = data_type.lower()
    if fmt not in _TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data type: {data_type!r}")

    try:
        if fmt == "json":
            # JSON deserialization is safe and built‑in
            return json.loads(input_data.decode("utf-8"))
        elif fmt == "xml":
            # Parse XML using the standard library ElementTree.
            # ET.fromstring is safe for well‑formed XML and does not
            # resolve external entities (XXE protection).
            return ET.fromstring(input_data.decode("utf-8"))
    except Exception as exc:
        # Wrap any parsing error in a ValueError to avoid leaking low‑level details
        raise ValueError(f"Failed to deserialize data as {data_type}: {exc}") from exc