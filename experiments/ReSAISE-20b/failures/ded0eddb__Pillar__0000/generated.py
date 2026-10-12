import json
import xml.etree.ElementTree as ET
from typing import Any

# Define a whitelist of safe formats.
ALLOWED_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        The serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format}")

    try:
        if fmt == "json":
            # json.loads accepts a string; decode bytes to UTF-8.
            return json.loads(bytes_data.decode("utf-8"))
        elif fmt == "xml":
            # Parse XML into an ElementTree. Returning the root element.
            return ET.fromstring(bytes_data)
    except Exception as exc:
        # Wrap any exception to avoid leaking low‑level details.
        raise ValueError(f"Deserialization error for format '{data_format}': {exc}") from exc