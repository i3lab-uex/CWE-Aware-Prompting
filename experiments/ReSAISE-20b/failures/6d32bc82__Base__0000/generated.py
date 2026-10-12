import json

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object using only
    whitelisted, safe serialization formats.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or unsafe.
    """
    # Whitelist of safe formats
    _ALLOWED_FORMATS = {
        'json': json.loads,
    }

    fmt_lower = serialization_format.strip().lower()
    if fmt_lower not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: '{serialization_format}'")

    # Decode bytes to string before deserialization
    try:
        text = stream.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Stream is not valid UTF-8 encoded text.") from exc

    # Perform deserialization
    try:
        return _ALLOWED_FORMATS[fmt_lower](text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to deserialize JSON data.") from exc