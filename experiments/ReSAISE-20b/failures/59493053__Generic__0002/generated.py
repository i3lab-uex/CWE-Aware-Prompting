import json
from xml.etree import ElementTree as ET
from io import BytesIO

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Deserialize `input_data` according to the specified format.

    Supported formats (safe):
        - 'json': JSON text encoded in UTF‑8
        - 'xml' : XML document

    Any other format will raise a ValueError.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte form.
    serialization_format : str
        Identifier of the serialization format.

    Returns
    -------
    Any
        The deserialized Python object.
    """
    # Normalise the format string
    fmt = serialization_format.strip().lower()

    if fmt == 'json':
        try:
            text = input_data.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    elif fmt == 'xml':
        try:
            # ElementTree can parse from a file-like object
            return ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    else:
        # Disallow pickle and any other potentially unsafe formats
        raise ValueError(f"Unsupported or dangerous format: {serialization_format}")