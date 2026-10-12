import json
import xml.etree.ElementTree as ET
import pickle

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Safely deserialize data from a supported format.

    Parameters
    ----------
    encoded_data : bytes
        Serialized representation of the data.
    method : str
        One of: 'json', 'xml', or 'pickle'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unsupported or potentially dangerous.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise ValueError("encoded_data must be bytes or bytearray")

    method = method.lower()
    if method == "json":
        try:
            # decode bytes to string using utf-8; errors='strict' ensures invalid data raises
            text = encoded_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == "xml":
        try:
            # ElementTree.fromstring parses XML without executing any code
            return ET.fromstring(encoded_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    elif method == "pickle":
        # Pickle is inherently unsafe with untrusted data.  Disallow it entirely.
        raise ValueError("Pickle deserialization is disallowed for untrusted data")

    else:
        raise ValueError(f"Unsupported serialization method: {method}")