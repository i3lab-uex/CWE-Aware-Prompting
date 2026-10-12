import json

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json",
}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        Serialized data to be deserialized.
    stream_format : str
        Format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    # Normalise format string to lower case and strip whitespace
    fmt = stream_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    try:
        # JSON expects a string; decode the bytes using UTF-8.
        decoded = stream.decode("utf-8")
        return json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc