import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Safely deserializes data from a limited set of formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte form.
    serialization_format : str
        One of the supported formats: 'json' or 'xml'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        # Decode bytes to string using UTF-8 (common encoding for JSON)
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8 for JSON") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "xml":
        # Parse XML safely. ElementTree does not resolve external entities by default.
        try:
            return ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Disallow pickle, yaml, msgpack, etc. to mitigate CWE-913.
        raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format}")