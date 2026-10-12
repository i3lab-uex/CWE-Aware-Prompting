import json

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object only for supported and secure formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        The format of the serialized data. Currently only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list, str, etc.).

    Raises
    ------
    ValueError
        If the data format is unsupported or considered insecure.
    """
    if not isinstance(byte_stream, (bytes, bytearray)):
        raise TypeError("byte_stream must be bytes or bytearray")

    if not isinstance(data_format, str):
        raise TypeError("data_format must be a string")

    fmt = data_format.strip().lower()

    if fmt == "json":
        # Decode bytes to string safely
        try:
            text = byte_stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode JSON bytes as UTF-8") from exc

        # json.loads is safe for untrusted input
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # If we reach here, the format is unsupported or insecure
    raise ValueError(f"Unsupported or insecure data format: {data_format!r}")