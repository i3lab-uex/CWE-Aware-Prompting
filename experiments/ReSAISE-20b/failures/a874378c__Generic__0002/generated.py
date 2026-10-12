import json

# Define the set of safe, supported formats.
SAFE_FORMATS = {"json"}

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object only for safe formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        Format identifier, e.g., 'json'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if data_format not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    # JSON is the only supported format. Decode bytes to str.
    try:
        text = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF-8 encoded JSON") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc