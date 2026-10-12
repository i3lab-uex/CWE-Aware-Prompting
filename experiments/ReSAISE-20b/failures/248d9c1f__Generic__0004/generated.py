import json
import xml.etree.ElementTree as ET

def data_to_object(byte_data: bytes, encoding_type: str):
    """
    Deserialize byte data into a Python object using only trusted formats.

    Supported formats:
        - 'json': JSON string (UTF‑8 encoded)
        - 'xml' : XML data parsed into an ElementTree.Element

    Parameters
    ----------
    byte_data : bytes
        Serialized data in binary form.
    encoding_type : str
        The serialization format: 'json' or 'xml'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    # Normalise encoding_type
    fmt = encoding_type.strip().lower()
    if fmt not in {"json", "xml"}:
        raise ValueError(f"Unsupported or unsafe format '{encoding_type}'. "
                         f"Allowed formats: json, xml.")

    try:
        # Convert bytes to string (assuming UTF‑8)
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF‑8.") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    # fmt == "xml"
    try:
        return ET.fromstring(text)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data.") from exc