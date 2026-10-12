import json

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object only if the format is
    explicitly marked as safe. Unsupported or insecure formats raise a
    ValueError.

    Parameters:
        byte_stream (bytes): Serialized data.
        data_format (str): Identifier of the serialization format
                           ('json', 'pickle', etc.).

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or considered insecure.
        json.JSONDecodeError: Propagated if JSON parsing fails.
    """
    # Normalise format string to lower case for comparison
    fmt = data_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    # At this point we only support JSON.
    try:
        text = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Byte stream is not valid UTF‑8: {exc}") from exc

    # json.loads will raise JSONDecodeError on malformed data.
    return json.loads(text)