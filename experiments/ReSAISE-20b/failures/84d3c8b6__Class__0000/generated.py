import json
import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Safely deserialize data from a restricted set of formats.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object in byte format.
    method : str
        Serialization format used: 'json', 'xml'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or dangerous.
    """
    if not isinstance(encoded_data, bytes):
        raise TypeError("encoded_data must be of type 'bytes'")

    method = method.lower()

    if method == "json":
        try:
            text = encoded_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            text = encoded_data.decode("utf-8")
            # ElementTree parses XML safely; it does not execute code.
            return ET.fromstring(text)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError("Invalid XML data") from exc

    # Any other method is disallowed
    raise ValueError(f"Unsupported or dangerous serialization format: {method}")