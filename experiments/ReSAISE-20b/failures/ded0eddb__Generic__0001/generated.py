import json
import xml.etree.ElementTree as ET
from typing import Any


def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        Raw serialized data.
    data_format : str
        Format used for serialization. Supported formats are:
            - 'json'  (JSON)
            - 'xml'   (XML)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_format` is not supported or the data cannot be parsed.
    """
    if not isinstance(bytes_data, (bytes, bytearray)):
        raise ValueError("Input must be bytes or bytearray.")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            text = bytes_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to parse JSON data.") from exc

    if fmt == "xml":
        try:
            return ET.fromstring(bytes_data)
        except ET.ParseError as exc:
            raise ValueError("Failed to parse XML data.") from exc

    # Reject all other formats explicitly
    raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")