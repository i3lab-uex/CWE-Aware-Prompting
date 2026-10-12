import json

# Only the following formats are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    stream_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS or if deserialization fails.
    """
    # Ensure we only process allowed formats
    fmt = stream_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    try:
        if fmt == "json":
            # Decode bytes to text before parsing
            text = stream.decode("utf-8")
            return json.loads(text)
    except Exception as exc:
        # Wrap any exception in ValueError to avoid leaking implementation details
        raise ValueError(f"Failed to deserialize {stream_format} data: {exc}") from exc