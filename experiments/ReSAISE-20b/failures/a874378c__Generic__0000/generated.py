import json

# A set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        Format identifier (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered insecure.
    """
    # Normalise format string to lower case for comparison
    fmt = data_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format}")

    # For JSON we need to decode bytes to a string
    try:
        decoded = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF-8") from exc

    # Parse JSON safely
    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc