import json

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data as a byte string.
    stream_format : str
        Identifier of the serialization format. Only formats listed in
        ``SAFE_FORMATS`` are allowed.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in ``SAFE_FORMATS``.
    TypeError
        If `stream` is not a bytes instance or if the data cannot be decoded.
    """
    # Validate input types
    if not isinstance(stream, bytes):
        raise TypeError(f"Expected 'bytes' for stream, got {type(stream).__name__}")

    # Normalize format string
    fmt = stream_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: '{stream_format}'")

    # Perform deserialization
    try:
        text = stream.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise TypeError(f"Stream could not be decoded as UTF-8: {exc}") from exc

    try:
        if fmt == "json":
            return json.loads(text)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize JSON content: {exc}") from exc

    # In theory unreachable because all supported formats are handled
    raise ValueError(f"Unhandled format: {stream_format}")