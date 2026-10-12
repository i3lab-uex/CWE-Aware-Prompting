import json
import xml.etree.ElementTree as ET
from typing import Any


def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte string into a Python object using only safe, permitted formats.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte format.
    serialization_format : str
        One of the supported formats: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        # json.loads expects a str, not bytes
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF‑8 JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        # Parse XML into a dictionary representation
        try:
            root = ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

        def elem_to_dict(elem):
            d = {elem.tag: {} if elem.attrib else None}
            children = list(elem)
            if children:
                dd = {}
                for child in children:
                    dd.update(elem_to_dict(child))
                d[elem.tag] = dd
            if elem.attrib:
                d[elem.tag].update({f"@{k}": v for k, v in elem.attrib.items()})
            text = elem.text.strip() if elem.text else None
            if text:
                d[elem.tag]["#text"] = text
            return d

        return elem_to_dict(root)

    # Disallow pickle, yaml, msgpack, etc.
    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")