import json

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object for a limited set of safe formats.

    Parameters
    ----------
    stream : bytes
        Serialized data in bytes.
    stream_format : str
        The format of the serialized data. Supported formats are:
        - 'json'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the stream_format is not supported or if deserialization fails.
    """
    # Only allow a whitelist of safe formats
    allowed_formats = {"json"}

    if stream_format not in allowed_formats:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    if not isinstance(stream, (bytes, bytearray)):
        raise ValueError("Stream must be a bytes-like object")

    try:
        # Decode the byte stream safely
        text = stream.decode("utf-8", errors="replace")
    except Exception as exc:
        raise ValueError(f"Failed to decode stream: {exc}") from exc

    try:
        if stream_format == "json":
            return json.loads(text)
    except Exception as exc:
        raise ValueError(f"Deserialization error: {exc}") from exc

    # Should never reach here due to the whitelist
    raise ValueError("Unhandled format during deserialization")