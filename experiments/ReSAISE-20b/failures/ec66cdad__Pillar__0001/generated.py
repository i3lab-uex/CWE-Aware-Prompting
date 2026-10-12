import json

# Define a whitelist of safe serialization formats.
ALLOWED_FORMATS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested serialization type is not in ALLOWED_FORMATS.
    """
    if serialization_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization type: {serialization_type}"
        )

    # For JSON, the input must be decoded to a string.
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF‑8 for JSON deserialization") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data") from exc