import json

# Define a whitelist of safe formats that are allowed for deserialization.
ALLOWED_FORMATS = {"json"}

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object corresponding to the input data.

    Raises
    ------
    ValueError
        If `data_format` is not in the whitelist of allowed formats.
    json.JSONDecodeError
        If the byte stream cannot be decoded as valid JSON (only for 'json' format).
    """
    # Normalise the format string: strip whitespace and lowercase
    fmt = data_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    # For the supported 'json' format, decode bytes to a string and parse.
    if fmt == "json":
        # Decode using UTF-8; raise UnicodeDecodeError on failure.
        text = byte_stream.decode("utf-8", errors="strict")
        # Use json.loads to parse the text into a Python object.
        return json.loads(text)

    # This point is unreachable due to the whitelist check, but kept for completeness.
    raise ValueError(f"Unhandled format: {data_format!r}")