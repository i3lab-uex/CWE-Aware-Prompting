import json
import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str):
    """
    Deserialize data from a known safe format.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object in byte form.
    method : str
        One of 'json' or 'xml'.  All other values raise ValueError.

    Returns
    -------
    object
        The deserialized Python object.  For JSON this is a native
        Python data structure; for XML it is an ElementTree.Element.

    Raises
    ------
    ValueError
        If the supplied method is not in the whitelist of allowed formats.
    """
    if method.lower() == "json":
        # JSON is safe when decoded via the standard library
        try:
            text = encoded_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method.lower() == "xml":
        # ElementTree provides a safe parser for XML that does not
        # execute code or load external entities by default.
        try:
            return ET.fromstring(encoded_data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Any other method is disallowed for security reasons
    raise ValueError(f"Unsupported or dangerous serialization format: {method!r}")