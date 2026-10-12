import json
from xml.etree import ElementTree as ET

def objectify_data(raw_data: bytes, method_name: str):
    """
    Deserialize a byte-encoded payload into a Python object in a secure way.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    method_name : str
        Serialization format used. Supported values are:
            * 'json'  - JSON encoded string.
            * 'xml'   - XML document.

    Returns
    -------
    Any
        The deserialized Python object. For JSON it is a native data structure.
        For XML it is an :class:`xml.etree.ElementTree.Element` tree.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    # Supported formats mapping to safe handlers
    _FORMAT_HANDLERS = {
        'json': _deserialize_json,
        'xml' : _deserialize_xml,
    }

    # Normalise method name
    key = method_name.lower()
    if key not in _FORMAT_HANDLERS:
        raise ValueError(f"Unsupported or dangerous format: {method_name!r}")

    handler = _FORMAT_HANDLERS[key]
    return handler(raw_data)


def _deserialize_json(raw: bytes):
    """Deserialize JSON from UTF-8 encoded bytes."""
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("JSON payload is not valid UTF-8") from exc

    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Failed to decode JSON") from exc


def _deserialize_xml(raw: bytes):
    """Deserialize XML into an ElementTree.  No eval or code execution."""
    try:
        return ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError("Failed to parse XML") from exc