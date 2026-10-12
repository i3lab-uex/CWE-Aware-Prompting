import json

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is unsupported or insecure.
    """
    # Normalise format string to lowercase for comparison
    fmt = data_format.lower()

    if fmt == "json":
        # Decode bytes to string using UTF-8 (common for JSON)
        try:
            text = byte_stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte stream is not valid UTF-8 for JSON") from exc

        # Use json.loads with strict mode; it only creates basic Python types
        try:
            return json.loads(text, strict=True)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # If any other format is requested, reject it to avoid insecure deserialization
    raise ValueError(f"Unsupported or insecure data format: {data_format}")