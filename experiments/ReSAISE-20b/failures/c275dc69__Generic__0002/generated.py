import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream to deserialize.
    stream_format : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Normalize format string for case-insensitive comparison
    fmt = stream_format.strip().lower()

    if fmt != 'json':
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    # Convert bytes to text assuming UTF-8 encoding
    try:
        data_str = serialized_data.decode('utf-8')
    except Exception as exc:
        raise ValueError("Failed to decode bytes as UTF‑8") from exc

    # Use json.loads for safe deserialization
    try:
        return json.loads(data_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc