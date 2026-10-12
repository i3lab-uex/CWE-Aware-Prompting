import json
import xml.etree.ElementTree as ET
from typing import Any, Union


def _safe_json_loads(data: bytes) -> Any:
    """Deserialize JSON data from bytes safely."""
    try:
        # Decode UTF-8 and parse
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON data") from exc


def _safe_xml_loads(data: bytes) -> ET.Element:
    """Deserialize XML data from bytes safely."""
    try:
        # Decode UTF-8 and parse
        return ET.fromstring(data.decode("utf-8"))
    except (UnicodeDecodeError, ET.ParseError) as exc:
        raise ValueError("Invalid XML data") from exc


def deserialize_data(input_data: bytes, serialization_format: str) -> Union[Any, ET.Element]:
    """
    Deserialize data from a trusted set of formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    serialization_format : str
        One of 'json', 'xml'.

    Returns
    -------
    Any | xml.etree.ElementTree.Element
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        return _safe_json_loads(input_data)
    elif fmt == "xml":
        return _safe_xml_loads(input_data)

    # Disallow all other formats (including pickle, marshal, yaml, etc.)
    raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format}")