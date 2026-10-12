import json

# List of formats that are considered safe for deserialization.
_SAFE_FORMATS = {"json"}

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Supported formats are defined in
        `_SAFE_FORMATS`.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not supported or if deserialization fails.
    """
    # Normalise and validate the requested format
    fmt = data_format.strip().lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    # Only 'json' is supported in this safe implementation
    try:
        if fmt == "json":
            # JSON data is expected to be UTF‑8 encoded
            text = byte_stream.decode("utf-8")
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data as {data_format!r}: {exc}") from exc