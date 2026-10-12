import json
import xml.etree.ElementTree as ET

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json", "xml"}

def _parse_json(data: str):
    """Parse JSON data into Python objects."""
    return json.loads(data)

def _parse_xml(element: ET.Element):
    """
    Convert an ElementTree element into a nested dictionary.
    This is a simple conversion; for complex XML it may need to be extended.
    """
    def _element_to_dict(el):
        d = {el.tag: {} if el.attrib else None}
        children = list(el)
        if children:
            dd = {}
            for child in children:
                dd.update(_element_to_dict(child))
            d[el.tag] = dd
        if el.attrib:
            d[el.tag].update(("@"+k, v) for k, v in el.attrib.items())
        text = el.text.strip() if el.text else ""
        if text:
            d[el.tag]["#text"] = text
        return d

    return _element_to_dict(element)

def safe_deserialize(serialized_bytes: bytes, allowed_format: str):
    """
    Safely deserialize the given byte string into a Python object.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte string containing the serialized data.
    allowed_format : str
        One of 'json' or 'xml'. Other values raise ValueError.

    Returns
    -------
    Any
        The deserialized Python object (dict, list, str, etc.).

    Raises
    ------
    ValueError
        If the format is not in the list of safe formats.
    """
    fmt = allowed_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format}")

    try:
        if fmt == "json":
            # JSON is text-based; decode using UTF-8
            text = serialized_bytes.decode("utf-8")
            return _parse_json(text)
        elif fmt == "xml":
            # XML is also text-based; decode using UTF-8
            text = serialized_bytes.decode("utf-8")
            root = ET.fromstring(text)
            return _parse_xml(root)
    except Exception as exc:
        # Wrap any parsing exception in a ValueError to avoid leaking details
        raise ValueError(f"Deserialization error: {exc}") from None

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     json_bytes = b'{"key": "value", "list": [1, 2, 3]}'
#     xml_bytes = b'<root><item>value</item></root>'
#     print(safe_deserialize(json_bytes, "json"))
#     print(safe_deserialize(xml_bytes, "xml"))