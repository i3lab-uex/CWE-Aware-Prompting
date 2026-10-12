import json
import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Safely deserialize data from a known set of formats.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object in byte format.
    method : str
        The serialization method used: 'json', 'xml' or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    # Normalise method name to lower case
    fmt = method.lower()

    if fmt == "json":
        # json is safe for untrusted input
        try:
            text = encoded_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif fmt == "xml":
        # XML can be parsed safely into an ElementTree element.
        try:
            return ET.fromstring(encoded_data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    elif fmt == "pickle":
        # pickle is explicitly disallowed due to security risks
        raise ValueError("Deserialization of 'pickle' data is forbidden for security reasons.")

    else:
        raise ValueError(f"Unsupported serialization format: {method!r}")