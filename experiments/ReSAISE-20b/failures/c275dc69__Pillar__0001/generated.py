import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe,
    predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream that was previously serialized.
    stream_format : str
        The format used for serialization. Supported values are:
            - 'json'   (case-insensitive)

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If *stream_format* is unsupported or considered insecure.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise ValueError("serialized_data must be bytes or bytearray")

    fmt = stream_format.lower()
    if fmt == "json":
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc
    else:
        # Any other format (pickle, html, etc.) is disallowed for security reasons.
        raise ValueError(f"Unsupported or insecure format: {stream_format}")