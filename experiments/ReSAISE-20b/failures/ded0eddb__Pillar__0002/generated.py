import json
import xml.etree.ElementTree as ET

# Allowed serialization formats for safe deserialization
ALLOWED_FORMATS = {"json", "xml"}

def _parse_xml(data: str) -> ET.Element:
    """
    Parse XML data into an ElementTree.Element using a safe parser.
    The built‑in XMLParser does not resolve external entities by default,
    mitigating the risk of XXE attacks.
    """
    parser = ET.XMLParser()
    return ET.fromstring(data, parser=parser)

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize ``bytes_data`` according to ``data_format``.

    Parameters
    ----------
    bytes_data : bytes
        Raw serialized data.
    data_format : str
        The format used for serialization. Must be one of the values in
        ``ALLOWED_FORMATS``; otherwise a ValueError is raised.

    Returns
    -------
    object
        The deserialized Python data structure. For JSON, a native Python
        dict/list/str/int/etc.  For XML, an :class:`xml.etree.ElementTree.Element`
        instance representing the root element.

    Raises
    ------
    ValueError
        If ``data_format`` is not in the allowed list.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format}")

    # Decode bytes to text.  UTF‑8 is the de‑facto standard for both JSON and XML.
    try:
        text = bytes_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF‑8") from exc

    if fmt == "json":
        return json.loads(text)
    elif fmt == "xml":
        return _parse_xml(text)

# Example usage (commented out; remove comments to test):
# if __name__ == "__main__":
#     json_bytes = b'{"key": "value", "list": [1, 2, 3]}'
#     xml_bytes = b'<root><child>text</child></root>'
#
#     print(load_serialized_data(json_bytes, "json"))
#     root = load_serialized_data(xml_bytes, "xml")
#     print(ET.tostring(root).decode())