import json

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized data to deserialize.
    stream_format : str
        The format of the serialized data. Must be one of the safe formats.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered insecure.
    TypeError
        If the input stream is not bytes.
    """
    if not isinstance(stream, bytes):
        raise TypeError("stream must be of type 'bytes'")

    fmt = stream_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    # For JSON, decode the bytes to a string and parse it.
    try:
        text = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("stream contains invalid UTF‑8 data") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("invalid JSON data") from exc