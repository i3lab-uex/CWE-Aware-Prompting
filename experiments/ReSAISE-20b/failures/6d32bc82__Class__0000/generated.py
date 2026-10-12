import json

# Only these formats are considered safe for deserialization.
ALLOWED_FORMATS = {
    "json": json.loads,
}

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the specified format is not supported or considered unsafe.
    """
    if serialization_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {serialization_format!r}"
        )

    # Decode the bytes using UTF-8 (most common for text-based formats).
    try:
        decoded = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Stream is not valid UTF-8 encoded data.") from exc

    # Deserialize using the chosen safe deserializer.
    try:
        return ALLOWED_FORMATS[serialization_format.lower()](decoded)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception in a ValueError to avoid leaking implementation details.
        raise ValueError(f"Deserialization failed: {exc}") from exc