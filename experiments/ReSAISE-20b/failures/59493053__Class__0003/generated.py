import json
import xml.etree.ElementTree as ET

def _safe_json_loads(data: bytes):
    """
    Safely decode JSON data from a byte string.
    Only primitive types and containers are allowed by the json module itself,
    so no further checks are necessary here.
    """
    text = data.decode("utf-8")
    return json.loads(text)

def _safe_xml_parse(data: bytes):
    """
    Safely parse XML data from a byte string.
    The standard library's ElementTree parser does not execute code, but
    we still reject malformed XML to avoid denial‑of‑service attacks.
    """
    return ET.fromstring(data)

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Deserialize `input_data` according to the specified `serialization_format`.

    Supported formats: 'json', 'xml'.
    Unsupported or potentially dangerous formats (e.g. 'pickle') raise a ValueError.

    Parameters
    ----------
    input_data : bytes
        Serialized object in byte form.
    serialization_format : str
        The format used for serialization ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python object (dict, list, str, etc. for JSON; ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the format is unsupported or deemed dangerous.
    """
    fmt = serialization_format.lower()
    if fmt == "json":
        return _safe_json_loads(input_data)
    elif fmt == "xml":
        return _safe_xml_parse(input_data)
    else:
        # Reject any format that could execute code or be unsafe.
        raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format}")