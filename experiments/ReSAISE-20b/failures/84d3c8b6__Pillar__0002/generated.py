import json
import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Deserialize data from a restricted set of formats.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object represented in byte format.
    method : str
        Format used for serialization. Supported values are:
            'json'  - JSON format.
            'xml'   - XML format (parsed into an ElementTree element).
        Any other value will raise a ValueError.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an unsupported or dangerous format is requested.
    """
    if not isinstance(encoded_data, (bytes, bytearray)):
        raise TypeError("encoded_data must be bytes or bytearray")

    method = method.lower()
    try:
        text = encoded_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if method == "json":
        # json.loads is safe for untrusted input
        return json.loads(text)

    if method == "xml":
        # ElementTree's fromstring is safe for typical XML data.
        # It does not resolve external entities, mitigating XXE risks.
        return ET.fromstring(text)

    # Disallow pickle and any other potentially dangerous formats
    raise ValueError(f"Unsupported or unsafe serialization format: {method}")