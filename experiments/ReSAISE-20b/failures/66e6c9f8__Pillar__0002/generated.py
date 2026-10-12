import json

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object for supported formats.

    Parameters
    ----------
    stream : bytes
        The serialized data to be deserialized.
    stream_format : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the stream_format is not supported or if deserialization fails.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json"}

    fmt_lower = stream_format.strip().lower()
    if fmt_lower not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    # JSON deserialization
    try:
        text = stream.decode("utf-8")
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc