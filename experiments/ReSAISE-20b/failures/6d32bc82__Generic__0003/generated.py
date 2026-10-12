import json

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object using only
    supported and safe formats.

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
        If the format is unsupported or considered unsafe.
    """
    # Define the set of safe formats
    _SAFE_FORMATS = {
        "json": json.loads,
    }

    fmt = serialization_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe deserialization format: {serialization_format}"
        )

    # Convert bytes to string using UTF-8 (common for JSON)
    try:
        text = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Stream is not valid UTF-8 encoded data.") from exc

    # Perform deserialization
    try:
        return _SAFE_FORMATS[fmt](text)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data: {exc}") from exc