import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Deserialize a byte string into a Python object using only trusted formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        The serialization format. Supported values are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a native Python data structure.
        For XML, an `xml.etree.ElementTree.Element` instance representing the root.

    Raises
    ------
    ValueError
        If `data_type` is not one of the supported formats or if deserialization fails.
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be a bytes object")

    # Normalize the format string
    fmt = data_type.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF-8; raise if invalid encoding
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 encoding for JSON data") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data") from exc

    elif fmt == "xml":
        try:
            # ElementTree can parse bytes directly
            return ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError("Failed to parse XML data") from exc

    else:
        # Explicitly reject unsafe formats such as pickle, marshal, etc.
        raise ValueError(f"Unsupported or potentially dangerous format: {data_type!r}")