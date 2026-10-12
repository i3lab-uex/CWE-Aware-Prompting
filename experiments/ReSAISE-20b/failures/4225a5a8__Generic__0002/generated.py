import json
import xml.etree.ElementTree as ET

def objectify_data(raw_data: bytes, method_name: str):
    """
    Deserialize *raw_data* into a Python object based on the specified
    serialization method. Only `json` and `xml` are permitted. Any other
    method, including `pickle`, raises a ValueError.

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte form.
    method_name : str
        Name of the serialization format: 'json', 'xml' or any other.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *method_name* is not one of the allowed formats.
    """
    # Ensure input is bytes
    if not isinstance(raw_data, (bytes, bytearray)):
        raise TypeError("raw_data must be bytes-like")

    method_name = method_name.lower()

    if method_name == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method_name == "xml":
        try:
            # ElementTree parses XML safely; no external code execution
            return ET.fromstring(raw_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Disallow pickle and any other potentially unsafe formats
        raise ValueError(f"Unsupported or dangerous format: {method_name}")