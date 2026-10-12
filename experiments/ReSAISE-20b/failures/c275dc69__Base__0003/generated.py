import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The data to be deserialized.
    stream_format : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Only allow safe, predefined formats
    allowed_formats = {"json"}

    fmt = stream_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    # Decode bytes to string (UTF-8 is the default for JSON)
    try:
        text = serialized_data.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode data: {exc}") from exc

    # Use json.loads which only handles basic JSON types
    try:
        return json.loads(text)
    except Exception as exc:
        raise ValueError(f"Failed to parse JSON: {exc}") from exc