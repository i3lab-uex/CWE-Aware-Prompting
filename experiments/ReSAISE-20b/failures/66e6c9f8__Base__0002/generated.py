import json

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    stream_format : str
        The format of the serialized data. Only safe formats are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS.
    """
    if stream_format.lower() not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    # For JSON we expect UTF‑8 encoded text.
    try:
        decoded = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Stream is not valid UTF‑8 encoded JSON") from exc

    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data") from exc