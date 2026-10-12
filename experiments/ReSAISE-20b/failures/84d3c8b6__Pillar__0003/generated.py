import json
import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Deserialize a byte string into a Python object using the specified safe format.

    Parameters
    ----------
    encoded_data : bytes
        The serialized data.
    method : str
        One of 'json', 'xml'.  Pickle and other formats are disallowed.

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict for JSON, ElementTree.Element for XML).

    Raises
    ------
    ValueError
        If the method is unsupported or dangerous.
    """
    # Ensure we have a bytes object; if not, raise immediately
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise ValueError("encoded_data must be bytes or bytearray")

    # Decode to string using UTF-8, ignoring errors to avoid crashes
    try:
        text = encoded_data.decode('utf-8', errors='strict')
    except UnicodeDecodeError as exc:
        raise ValueError("Encoded data is not valid UTF-8") from exc

    method = method.lower()
    if method == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == 'xml':
        try:
            # ElementTree.parse requires a file-like object; use fromstring
            return ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Any other method is considered unsafe or unsupported
        raise ValueError(f"Unsupported deserialization format: {method!r}")