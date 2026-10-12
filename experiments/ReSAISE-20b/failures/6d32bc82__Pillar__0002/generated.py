import json

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object using only
    whitelisted, safe serialization formats.

    Parameters
    ----------
    stream : bytes
        The serialized data to be deserialized.
    serialization_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested, or if deserialization fails.
    """
    # Whitelist of safe formats
    allowed_formats = {
        'json': _deserialize_json,
    }

    # Normalize format string
    fmt_key = serialization_format.strip().lower()
    if fmt_key not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    # Call the appropriate deserializer
    try:
        return allowed_formats[fmt_key](stream)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data using format {serialization_format!r}: {exc}") from exc


def _deserialize_json(stream: bytes):
    """Deserialize JSON data from a byte stream."""
    # Decode to text, assuming UTF-8 (common for JSON)
    text = stream.decode('utf-8')
    return json.loads(text)