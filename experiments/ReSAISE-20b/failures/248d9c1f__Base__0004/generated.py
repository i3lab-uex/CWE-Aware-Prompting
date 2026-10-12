import json
import xml.etree.ElementTree as ET
from typing import Any

# Allowed, trusted serialization formats
_TRUSTED_FORMATS = {"json", "xml"}


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using only
    trusted serialization formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data in binary form.
    encoding_type : str
        Serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or dangerous.
    """
    if encoding_type.lower() not in _TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {encoding_type}")

    # Decode bytes to string using UTF-8 (common safe encoding)
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF-8") from exc

    if encoding_type.lower() == "json":
        # json.loads only parses basic data types (dict, list, str, int, float, bool, None)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if encoding_type.lower() == "xml":
        # Parse XML into ElementTree; convert to a simple nested dict representation
        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

        def _element_to_dict(elem):
            d = {}
            # include attributes
            if elem.attrib:
                d.update({f"@{k}": v for k, v in elem.attrib.items()})
            # include text
            if elem.text and elem.text.strip():
                d["#text"] = elem.text.strip()
            # include children
            for child in elem:
                child_dict = _element_to_dict(child)
                tag = child.tag
                if tag in d:
                    # ensure list for repeated tags
                    if not isinstance(d[tag], list):
                        d[tag] = [d[tag]]
                    d[tag].append(child_dict)
                else:
                    d[tag] = child_dict
            return d

        return {root.tag: _element_to_dict(root)}

    # This point should never be reached due to earlier check
    raise ValueError(f"Unhandled format: {encoding_type}")