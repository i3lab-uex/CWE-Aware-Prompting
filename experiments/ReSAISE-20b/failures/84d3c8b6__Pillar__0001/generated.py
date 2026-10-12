import json
import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Safely deserialize data from a supported format.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object in byte form.
    method : str
        Serialization format. Only 'json' and 'xml' are accepted.

    Returns
    -------
    Any
        The deserialized Python object. For JSON this is a dict/list/primitive.
        For XML this is an ``xml.etree.ElementTree.Element`` instance.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    # Normalise method name to lower case
    fmt = method.strip().lower()

    if fmt == 'json':
        # JSON is safe; decode bytes to text and parse
        try:
            text = encoded_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF‑8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == 'xml':
        # XML is safe for parsing into ElementTree; no eval or code execution
        try:
            text = encoded_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("XML data is not valid UTF‑8") from exc
        try:
            return ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Explicitly reject pickle or any other format to avoid code execution
        raise ValueError(f"Unsupported or dangerous serialization method: {method!r}")