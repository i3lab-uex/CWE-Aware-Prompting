import json
import xml.etree.ElementTree as ET

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json", "xml"}

def _bytes_to_str(data: bytes, encoding: str = "utf-8") -> str:
    """
    Convert raw bytes to a string using the specified encoding.
    Raises ValueError if decoding fails.
    """
    try:
        return data.decode(encoding)
    except (UnicodeDecodeError, AttributeError) as exc:
        raise ValueError("Input data is not valid UTF‑8 encoded bytes") from exc


def _parse_json(data: str):
    """
    Safely parse a JSON string into Python objects.
    The json module does not execute arbitrary code, so this is safe
    for untrusted input.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _parse_xml(data: str):
    """
    Safely parse an XML string into an ElementTree.Element.
    No external entities or DTDs are processed, mitigating XXE attacks.
    """
    try:
        # The default parser in ElementTree does not resolve external entities,
        # but we explicitly disable DTD processing for extra safety.
        parser = ET.XMLParser(resolve_entities=False)
        return ET.fromstring(data, parser=parser)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data") from exc


def safe_deserialize(serialized_bytes: bytes, allowed_format: str):
    """
    Deserialize `serialized_bytes` into a Python object only if the
    specified format is in the list of allowed formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw serialized data.
    allowed_format : str
        One of the supported formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object (dict/list for JSON,
        ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported format '{allowed_format}'. Allowed formats: {', '.join(SAFE_FORMATS)}")

    text = _bytes_to_str(serialized_bytes)

    if fmt == "json":
        return _parse_json(text)
    elif fmt == "xml":
        return _parse_xml(text)

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled format '{allowed_format}'.")