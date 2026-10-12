import json
from typing import Any

# Optional: use PyYAML if available, otherwise fall back to json only
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

import xml.etree.ElementTree as ET


def _safe_xml_deserialize(data: bytes) -> Any:
    """
    Convert XML bytes to a Python dictionary.  Only simple structures
    are supported – attributes and text values.
    """
    root = ET.fromstring(data)
    def _elem_to_dict(elem):
        d: dict[str, Any] = {}
        if elem.attrib:
            d.update({f"@{k}": v for k, v in elem.attrib.items()})
        if elem.text and elem.text.strip():
            d["#text"] = elem.text.strip()
        for child in elem:
            child_dict = _elem_to_dict(child)
            tag = child.tag
            if tag in d:
                # If the same tag appears multiple times, store as a list
                if not isinstance(d[tag], list):
                    d[tag] = [d[tag]]
                d[tag].append(child_dict)
            else:
                d[tag] = child_dict
        return d

    return {root.tag: _elem_to_dict(root)}


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize *byte_data* according to *encoding_type*, but only for
    a restricted set of safe formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    encoding_type : str
        One of 'json', 'yaml', or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or the data cannot be parsed.
    """
    if not isinstance(byte_data, bytes):
        raise ValueError("byte_data must be of type 'bytes'")

    enc = encoding_type.lower()
    if enc == "json":
        try:
            return json.loads(byte_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if enc == "yaml":
        if yaml is None:
            raise ValueError("PyYAML not installed – YAML support unavailable")
        try:
            return yaml.safe_load(byte_data.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError("Invalid YAML data") from exc

    if enc == "xml":
        try:
            return _safe_xml_deserialize(byte_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # All other formats are considered unsafe
    raise ValueError(f"Unsupported or dangerous serialization format: {encoding_type}")