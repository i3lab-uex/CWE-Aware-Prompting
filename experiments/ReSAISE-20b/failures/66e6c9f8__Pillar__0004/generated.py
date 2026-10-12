import json

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only supported,
    secure formats.

    Parameters
    ----------
    stream : bytes
        The serialized data to deserialize.
    stream_format : str
        Format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Normalize format string to lowercase and strip whitespace
    fmt = stream_format.strip().lower()

    if fmt != "json":
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    # Decode bytes to string using UTF-8 (the standard for JSON)
    try:
        text = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Stream is not valid UTF-8 encoded JSON") from exc

    # Parse the JSON safely
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc