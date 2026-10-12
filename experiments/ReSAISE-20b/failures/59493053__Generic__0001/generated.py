import json
import xml.etree.ElementTree as ET
from typing import Any, Union


def _safe_json_loads(data: bytes) -> Any:
    """Deserialize JSON data from bytes."""
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON data") from exc


def _safe_xml_parse(data: bytes) -> ET.Element:
    """Deserialize XML data from bytes. Returns the root Element."""
    try:
        # `ET.fromstring` does not support external entities by default,
        # which mitigates XXE attacks. The parser is also limited to
        # standard XML and will raise an error for malformed input.
        return ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data") from exc


def deserialize_data(
    input_data: bytes, serialization_format: str
) -> Union[Any, ET.Element]:
    """
    Deserialize data from the given format.

    Supported formats: 'json', 'xml'.
    Unsupported or dangerous formats raise ValueError.

    Parameters
    ----------
    input_data : bytes
        Serialized object in byte form.
    serialization_format : str
        The format used for serialization.

    Returns
    -------
    Any
        Deserialized Python object or an ElementTree.Element for XML.

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        return _safe_json_loads(input_data)
    elif fmt == "xml":
        return _safe_xml_parse(input_data)
    else:
        # Disallow pickle and any other format that could be unsafe
        raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format}")