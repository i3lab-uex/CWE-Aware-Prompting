import json

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object in a secure manner.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Only a whitelist of safe formats is allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Define a whitelist of safe formats. Extend this list only when you are certain
    # the format can be safely parsed without side effects.
    SAFE_FORMATS = {"json"}

    if data_format.lower() not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    # Decode the byte stream safely. Use UTF-8 as it is the de facto standard for JSON.
    try:
        text = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF-8 encoded data") from exc

    # Perform the actual deserialization. json.loads is safe for arbitrary input
    # as it only builds basic Python data structures.
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to decode JSON") from exc