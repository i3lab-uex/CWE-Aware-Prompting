import json

__all__ = ["deserialize_stream_data"]

# Only these formats are considered safe for deserialization
_ALLOWED_FORMATS = {"json"}


def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested, or if the stream cannot be decoded.
    """
    fmt = serialization_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    try:
        text = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Stream could not be decoded using UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc