import json
import xml.etree.ElementTree as ET
from typing import Any


def _parse_xml(data: bytes) -> Any:
    """
    Convert XML data into a nested dictionary.
    This is a very lightweight parser that only supports simple
    element/value pairs and ignores attributes. It is deliberately
    limited to avoid executing arbitrary code or accessing the
    filesystem.
    """
    root = ET.fromstring(data.decode("utf-8"))
    def _elem_to_dict(elem: ET.Element) -> Any:
        if len(elem) == 0:
            # No children – treat as a string value
            return elem.text or ""
        return {child.tag: _elem_to_dict(child) for child in elem}
    return {_elem_to_dict(root)}

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize `encoded_data` according to the specified `method`.

    Supported methods are:

    * ``json`` – JSON data using the standard library.
    * ``xml``  – Very small subset of XML, parsed into nested dicts.
      No support for attributes or namespaces to keep the parser simple
      and safe.

    The ``pickle`` format (and any other dynamic formats) are *not*
    supported because they can execute arbitrary code and therefore
    pose a security risk.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object represented in byte format.
    method : str
        One of ``'json'`` or ``'xml'``.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unsupported or potentially dangerous.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise TypeError("encoded_data must be bytes or bytearray")

    method = method.lower()
    if method == "json":
        try:
            return json.loads(encoded_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            return _parse_xml(encoded_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # Reject any other method, especially pickle
    raise ValueError(f"Unsupported or dangerous serialization format: {method}")