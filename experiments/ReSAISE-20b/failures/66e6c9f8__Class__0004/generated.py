import json

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        Serialized data.
    stream_format : str
        Format of the serialized data. Currently only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    TypeError
        If `stream` is not a bytes instance.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise TypeError("stream must be a bytes-like object")

    fmt = stream_format.lower()
    if fmt == 'json':
        try:
            return json.loads(stream.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc
    else:
        # Add additional safe formats here if needed.
        raise ValueError(f"Unsupported or insecure format: {stream_format}")