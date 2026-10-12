import json

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        Serialized data received from an external source.
    stream_format : str
        Format identifier of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    if not isinstance(stream, bytes):
        raise ValueError("Stream must be of type 'bytes'")

    if stream_format.lower() != "json":
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    try:
        # Decode bytes to string using UTF-8, then parse JSON
        decoded = stream.decode("utf-8")
    except (UnicodeDecodeError, AttributeError) as exc:
        raise ValueError("Failed to decode byte stream") from exc

    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc