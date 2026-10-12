import json

# Define the set of safe, supported formats for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object for supported formats.

    Parameters
    ----------
    stream : bytes
        Serialized data received from an external source.
    stream_format : str
        Format identifier of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object corresponding to the input data.

    Raises
    ------
    ValueError
        If `stream_format` is not in the set of supported safe formats,
        or if deserialization fails due to malformed data.
    """
    # Normalise the format string and validate it
    fmt = stream_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    # Decode the byte stream to a string using UTF-8
    try:
        data_str = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input stream is not valid UTF‑8 encoded data") from exc

    # Perform deserialization based on the format
    if fmt == "json":
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON data") from exc

    # In case new formats are added in the future, this point should never be reached
    raise ValueError(f"Unhandled format: {stream_format!r}")