import json
import xml.etree.ElementTree as ET
from typing import Any


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes raw bytes into a Python object based on the provided format.

    Parameters
    ----------
    raw_data : bytes
        The serialized data to be deserialized.
    serialization_format : str
        The format used for serialization. Supported values are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object. For JSON this will be a native Python data structure.
        For XML this will be an :class:`xml.etree.ElementTree.Element` instance.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is specified.
    """
    # Normalise the format string to avoid case‑sensitivity issues
    fmt = serialization_format.strip().lower()

    if fmt == "json":
        try:
            # JSON expects text, so decode bytes using UTF‑8
            text = raw_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "xml":
        try:
            # XML also expects text; decode using UTF‑8
            text = raw_data.decode("utf-8")
            return ET.fromstring(text)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # If we reach here, the format is not supported
    raise ValueError(
        f"Unsupported serialization format: '{serialization_format}'. "
        "Only 'json' and 'xml' are allowed."
    )